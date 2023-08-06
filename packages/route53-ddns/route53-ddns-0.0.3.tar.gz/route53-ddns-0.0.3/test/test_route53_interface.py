from route53_ddns import route53_interface
from unittest.mock import MagicMock, call, patch
import pytest


@patch("route53_ddns.route53_interface.route53")
def test_get_hosted_zone_id_raises_keyerror_if_no_zone(route53_mock):
    route53_mock.list_hosted_zones.return_value = {"HostedZones": []}

    with pytest.raises(KeyError):
        route53_interface.get_hosted_zone_id("my.zone")


@patch("route53_ddns.route53_interface.route53")
def test_get_hosted_zone_id_value_error_if_not_found(route53_mock):
    route53_mock.list_hosted_zones.return_value = {"HostedZones": [{"Name": "another.zone"}]}

    with pytest.raises(ValueError):
        route53_interface.get_hosted_zone_id("my.zone")


@patch("route53_ddns.route53_interface.route53")
def test_get_hosted_zone_id_returns_right_Value(route53_mock):
    route53_mock.list_hosted_zones.return_value = {"HostedZones": [{"Name": "my.zone.", "Id": "expected_id"}]}

    zone_id = route53_interface.get_hosted_zone_id("my.zone")
    assert zone_id == "expected_id"


@patch('route53_ddns.route53_interface.sleep')
@patch("route53_ddns.route53_interface.route53")
def test_wait_for_change_completion(route53_mock, sleep_mock):
    sleep_mock.return_value = None
    route53_mock.get_change.side_effect = [
        {"ChangeInfo": {"Status": "PENDING"}},
        {"ChangeInfo": {"Status": "PENDING"}},
        {"ChangeInfo": {"Status": "INSYNC"}},
    ]

    route53_interface.wait_for_change_completion(change_id="change_id")
    
    route53_mock.get_change.assert_has_calls([
        call(Id="change_id"),
        call(Id="change_id"),
        call(Id="change_id")
    ])


@patch("route53_ddns.route53_interface.route53")
def test_get_current_ip_not_found(route53_mock):
    route53_mock.list_resource_record_sets.return_value = {
        "ResourceRecordSets": [
            {
                "Name": "record.other.zone.",
                "Type": "CNAME",
                "TTL": 3600
            }
        ]
    }

    assert route53_interface.get_current_ip(zone_id="my.zone", record_name="record") == None


@patch("route53_ddns.route53_interface.route53")
def test_get_current_ip_found_wrong_type(route53_mock):
    route53_mock.list_resource_record_sets.return_value = {
        "ResourceRecordSets": [
            {
                "Name": "record.my.zone.",
                "Type": "CNAME",
                "TTL": 3600,
                "ResourceRecords": [{"Value": "other.domain"}]
            }
        ]
    }

    with pytest.raises(ValueError):
        route53_interface.get_current_ip(zone_id="my.zone", record_name="record.my.zone")


@patch("route53_ddns.route53_interface.route53")
def test_get_current_ip_too_many_entries(route53_mock):
    route53_mock.list_resource_record_sets.return_value = {
        "ResourceRecordSets": [
            {
                "Name": "record.my.zone.",
                "Type": "A",
                "TTL": 3600,
                "ResourceRecords": [{"Value": "10.0.0.1"}, {"Value": "10.0.0.2"}]
            }
        ]
    }

    with pytest.raises(ValueError):
        route53_interface.get_current_ip(zone_id="my.zone", record_name="record.my.zone")


@patch("route53_ddns.route53_interface.route53")
def test_get_current_ip_found_ok(route53_mock):
    route53_mock.list_resource_record_sets.return_value = {
        "ResourceRecordSets": [
            {
                "Name": "record.my.zone.",
                "Type": "A",
                "TTL": 3600,
                "ResourceRecords": [{"Value": "10.0.0.1"}]
            }
        ]
    }

    assert route53_interface.get_current_ip(zone_id="my.zone", record_name="record.my.zone") == "10.0.0.1"


@patch("route53_ddns.route53_interface.get_current_ip")
@patch("route53_ddns.route53_interface.get_hosted_zone_id")
@patch("route53_ddns.route53_interface.route53")
def test_update_record_nothing_to_do(route53_mock, get_hosted_zone_id_mock, get_current_ip_mock):
    get_hosted_zone_id_mock.return_value = "zone_id"
    get_current_ip_mock.return_value = "10.0.0.1"

    route53_interface.update_record("my.zone", "record.my.zone", "10.0.0.1")
    route53_mock.change_resource_record_sets.assert_not_called()


@patch("route53_ddns.route53_interface.get_current_ip")
@patch("route53_ddns.route53_interface.get_hosted_zone_id")
@patch("route53_ddns.route53_interface.route53")
def test_update_record_dryrun(route53_mock, get_hosted_zone_id_mock, get_current_ip_mock):
    get_hosted_zone_id_mock.return_value = "zone_id"
    get_current_ip_mock.return_value = "10.0.0.2"

    route53_interface.update_record("my.zone", "record.my.zone", "10.0.0.1", dryrun=True)
    route53_mock.change_resource_record_sets.assert_not_called()


@patch("route53_ddns.route53_interface.wait_for_change_completion")
@patch("route53_ddns.route53_interface.get_current_ip")
@patch("route53_ddns.route53_interface.get_hosted_zone_id")
@patch("route53_ddns.route53_interface.route53")
def test_update_record(route53_mock, get_hosted_zone_id_mock, get_current_ip_mock, wait_for_change_completion):
    get_hosted_zone_id_mock.return_value = "zone_id"
    get_current_ip_mock.return_value = "10.0.0.2"
    route53_mock.change_resource_record_sets.return_value = {"ChangeInfo": {"Id": "change-id"}}
    wait_for_change_completion.return_value = None

    route53_interface.update_record("my.zone", "record.my.zone", "10.0.0.1")

    route53_mock.change_resource_record_sets.assert_called_once_with(
        HostedZoneId="zone_id",
        ChangeBatch={
            "Comment": f"Updating record to 10.0.0.1",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": "record.my.zone",
                        "Type": "A",
                        "TTL": 60,
                        "ResourceRecords": [{"Value": "10.0.0.1"}],
                    },
                }
            ],
        },
    )
    wait_for_change_completion.assert_called_once()



