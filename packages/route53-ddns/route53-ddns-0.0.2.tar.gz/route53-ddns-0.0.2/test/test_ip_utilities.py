import socket
from route53_ddns import ip_utilities
from unittest.mock import call, patch, Mock


@patch('route53_ddns.ip_utilities.requests')
def test_get_ip_successful(requests_mock):
    response = Mock(content=b'{"ip": "10.0.0.1"}')
    requests_mock.get.return_value = response

    assert ip_utilities.get_ip() == "10.0.0.1"


@patch('route53_ddns.ip_utilities.sleep')
@patch('route53_ddns.ip_utilities.verify_propagation')
def test_wait_for_propagation_retries(verify_propagation_mock, sleep_mock):
    verify_propagation_mock.side_effect = [False, False, True]
    sleep_mock.return_value = None

    ip_utilities.wait_for_propagation("record", "10.0.0.1")

    verify_propagation_mock.assert_has_calls(
        [
            call(record="record", target_ip="10.0.0.1"),
            call(record="record", target_ip="10.0.0.1"),
            call(record="record", target_ip="10.0.0.1"),
        ]
    )


@patch('route53_ddns.ip_utilities.gethostbyname_ex')
def test_verify_propagation_not_propagated(gethostbyname_ex_mock):
    gethostbyname_ex_mock.side_effect = socket.gaierror("Not resolvable")

    assert ip_utilities.verify_propagation("record", "10.0.0.1") == False


@patch('route53_ddns.ip_utilities.gethostbyname_ex')
def test_verify_propagation_correct_ip(gethostbyname_ex_mock):
    gethostbyname_ex_mock.return_value = (None, None, ["10.0.0.1"])

    assert ip_utilities.verify_propagation("record", "10.0.0.1") == True


@patch('route53_ddns.ip_utilities.gethostbyname_ex')
def test_verify_propagation_incorrect_ip(gethostbyname_ex_mock):
    gethostbyname_ex_mock.return_value = (None, None, ["10.0.0.2"])

    assert ip_utilities.verify_propagation("record", "10.0.0.1") == False


@patch('route53_ddns.ip_utilities.gethostbyname_ex')
def test_verify_propagation_multiple_ip(gethostbyname_ex_mock):
    gethostbyname_ex_mock.return_value = (None, None, ["10.0.0.1", "10.0.0.2"])

    assert ip_utilities.verify_propagation("record", "10.0.0.1") == False
