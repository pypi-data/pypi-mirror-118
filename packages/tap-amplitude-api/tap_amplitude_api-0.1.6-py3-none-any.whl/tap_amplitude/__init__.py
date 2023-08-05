#!/usr/bin/env python3
import os
import json
import singer
from singer import utils, metadata, get_bookmark
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from io import BytesIO
from zipfile import ZipFile
from urllib import request
import base64
import gzip

from singer.transform import Transformer
from datetime import datetime, timedelta

AMPLITUDE_DATETIME_FORMAT = "%Y%m%dT%H"
BASE_AMPLITUDE_URL = "https://amplitude.com/api/2/export"

REQUIRED_CONFIG_KEYS = ["auth_user", "auth_password"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        # TODO: populate any metadata and stream's key properties here..
        stream_metadata = []
        key_properties = ["event_id"]
        replication_key = "server_upload_time"
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=replication_key,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def load_all_events(config, state, tap_stream_id):
    end_date = datetime.now()
    start_date_bookmark = singer.get_bookmark(state, tap_stream_id, 'event')
    if start_date_bookmark is None:
        start_date = end_date - timedelta(days=2)
    else:
        start_date = datetime.strptime(start_date_bookmark, '%Y-%m-%dT%H:%M:%S.%fZ')

    for n in range(int((end_date - start_date).days)):
        local_start = start_date + timedelta(days=n)
        local_end = start_date + timedelta(days=n+1)
        LOGGER.info(f'quering for a date range: ({local_start} : {local_end})')
        return load_events(config, local_start, local_end)


def load_events(config, start_date, end_date):
    start = start_date.strftime(AMPLITUDE_DATETIME_FORMAT)
    end = end_date.strftime(AMPLITUDE_DATETIME_FORMAT)

    url = f'{BASE_AMPLITUDE_URL}?start={start}&end={end}'
    LOGGER.info(f'Quering URL: {url}')
    auth_user = config.get("auth_user")
    auth_passwd = config.get("auth_password")
    base64string = base64.b64encode(('%s:%s' % (auth_user, auth_passwd)).encode('utf-8')).decode('utf-8').replace('\n', '')

    hdr = {
        "Authorization": f'Basic {base64string}'
    }
    req = request.Request(url, headers=hdr)

    resp = request.urlopen(req)
    zipfile = ZipFile(BytesIO(resp.read()))
    for file_name in zipfile.namelist():
        with zipfile.open(file_name) as gz_file:
            gz_content = gz_file.read()
            str_content = gzip.decompress(gz_content).decode("utf-8")
            lines = str_content.split("\n")
            for line in lines:
                if "" == line.strip():
                    continue
                yield json.loads(line)

def sync(config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    stream = catalog.get_stream("event")
    LOGGER.info("Syncing stream:" + stream.tap_stream_id)

    bookmark_column = stream.replication_key
    is_sorted = True  # TODO: indicate whether data is sorted ascending on bookmark value

    singer.write_schema(
        stream_name=stream.tap_stream_id,
        schema=stream.schema.to_dict(),
        key_properties=stream.key_properties,
    )

    tap_data = lambda: load_all_events(config, state, "event")

    max_bookmark = None
    with Transformer() as transformer:
        for row in tap_data():
            rec = transformer.transform(row, stream.schema.to_dict())
            singer.write_records(stream.tap_stream_id, [rec])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state({stream.tap_stream_id: rec[bookmark_column]})
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, rec[bookmark_column])

    if bookmark_column and not is_sorted:
        singer.write_state({stream.tap_stream_id: max_bookmark})
    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
