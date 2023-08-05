import requests
import re
from pathlib import Path
import time
from qualys_etl.etld_lib import etld_lib_credentials as etld_lib_credentials
from qualys_etl.etld_lib import etld_lib_config as etld_lib_config
from qualys_etl.etld_lib import etld_lib_functions as etld_lib_functions
from qualys_etl.etld_lib import etld_lib_extract_transform_load_distribute as etld_lib_extract_transform_load_distribute

global json_file
global url
global multi_proc_host_ids
global multi_proc_batch_number
global json_file_utc_run_datetime
global qualys_headers_multi_proc_dict


def asset_inventory_extract(asset_last_updated, last_seen_assetid, utc_datetime, batch_number, proc_dict):
    global json_file
    global url
    global multi_proc_host_ids
    global multi_proc_batch_number
    global json_file_utc_run_datetime
    global qualys_headers_multi_proc_dict

    qualys_headers_multi_proc_dict = proc_dict
    json_file_utc_run_datetime = utc_datetime
    multi_proc_batch_number = batch_number
    cred_dict = etld_lib_credentials.get_cred()
    bearer = etld_lib_credentials.get_bearer(update_bearer=False)
    url = f"https://{cred_dict['gateway_fqdn_server']}/rest/2.0/search/am/asset"
    # /rest/2.0/search/am/asset?assetLastUpdated=2021-06-01T00:00:00Z&lastSeenAssetId=0
    url = f"{url}?assetLastUpdated={asset_last_updated}&lastSeenAssetId={last_seen_assetid}"

    # payload = {'assetLastUpdated': asset_last_updated,
    #            'lastSeenAssetId': last_seen_assetid}

    headers = {'X-Requested-With': 'qualysetl', 'Authorization': bearer, 'Content-Type': 'application/json'}

#    print_payload = payload.copy()
    etld_lib_functions.logger.info(f"api call     - {url}")

    json_file_prefix = re.sub(".json$", "", str(etld_lib_config.asset_inventory_json_file))
    json_batch_assetLastUpdated = re.sub(':', '_', f"{asset_last_updated}")
    json_file_utc_run_datetime_filename = re.sub(':', '_', f"{json_file_utc_run_datetime}")
    json_file_name = f'{Path(json_file_prefix).name}_utc_run_datetime_{json_file_utc_run_datetime_filename}' \
                     f'_utc_assetLastUpdated_{json_batch_assetLastUpdated}' \
                     f'_{multi_proc_batch_number}.json'
    json_file = Path(etld_lib_config.asset_inventory_json_dir, json_file_name)

    chunk_size_calc = 20480
    try_extract_max_count = 5
    http_conn_timeout = 300
    etld_lib_extract_transform_load_distribute.extract_qualys(
        try_extract_max_count=try_extract_max_count,
        url=url,
        headers=headers,
        payload={},
        http_conn_timeout=http_conn_timeout,
        chunk_size_calc=chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_dict=qualys_headers_multi_proc_dict,
        multi_proc_batch_number=multi_proc_batch_number,
        extract_validation_type='json')


def get_qualys_limits_from_asset_inventory():
    global json_file
    global url
    global multi_proc_host_ids
    global multi_proc_batch_number
    global json_file_utc_run_datetime
    global qualys_headers_multi_proc_dict
    etld_lib_credentials.main()
    cred_dict = etld_lib_credentials.get_cred()
    authorization = cred_dict['authorization']  # Base64 user:password
    use_cookie = etld_lib_credentials.use_cookie  # If true, use cookie auth
    url = f"https://{cred_dict['api_fqdn_server']}/api/2.0/fo/asset/host/vm/detection/"

    payload = {'action': 'list',
               'truncation_limit': '1',
               }

    if use_cookie is False:
        headers = {'X-Requested-With': 'qualysetl', 'Authorization': authorization}
    else:
        headers = {'X-Requested-With': 'qualysetl', 'Cookie': etld_lib_credentials.cookie_file()}

    json_file = Path("/dev/null")
    chunk_size_calc = 20480
    try_extract_max_count = 3
    http_conn_timeout = 30
    multi_proc_batch_number = "check_headers"
    etld_lib_extract_transform_load_distribute.extract_qualys(
        try_extract_max_count=try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=http_conn_timeout,
        chunk_size_calc=chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_dict=qualys_headers_multi_proc_dict,
        multi_proc_batch_number=multi_proc_batch_number,
        extract_validation_type='json')


def start_msg_asset_inventory_extract():
    etld_lib_functions.logger.info(f"start")


def end_msg_asset_inventory_extract():
    global url
    global json_file
    global json_file_utc_run_datetime
    etld_lib_functions.log_file_info(url, 'in')
    etld_lib_functions.logger.info(f"Run Date: {json_file_utc_run_datetime}")
    etld_lib_functions.log_file_info(json_file)
    etld_lib_functions.logger.info(f"end")


def main(args=None):
    start_msg_asset_inventory_extract()
    etld_lib_credentials.main()
    asset_inventory_extract()
    end_msg_asset_inventory_extract()


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='asset_inventory_extract')
    etld_lib_config.main()
    etld_lib_credentials.main()
    main()



