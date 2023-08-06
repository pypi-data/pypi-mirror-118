# route53-ddns

This package provide a simple CLI to update a Route53 Hosted Zone. This can be run as
cron job to provide a dynamic DNS functionality.

The package uses [ipify](https://www.ipify.org) to get the current IP (or it can be provided as argument).

Route53 interaction is achieved using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
Credentials can be provided in any of the supported way boto3 expects them.
See [boto3 credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)
documentation.

## Usage

To update the record `home.example.com`, giving you have an `example.com` hosted zone in your AWS account:

```bash
$ route53-ddns --zone example.com --record home
2021-09-02 22:09:18,289 - root - INFO - Adjusting target record to be home.example.com
2021-09-02 22:09:18,683 - route53_ddns.ip_utilities - INFO - Detected IP 107.3.160.43
2021-09-02 22:09:19,100 - route53_ddns.route53_interface - INFO - Found zone /hostedzone/XXXXXXXXXXXXXX with name example.com. matching the expected example.com
2021-09-02 22:09:19,100 - route53_ddns.route53_interface - INFO - Checking current records
2021-09-02 22:09:19,437 - route53_ddns.route53_interface - INFO - Found record of type NS with ttl 172800 named example.com.
2021-09-02 22:09:19,437 - route53_ddns.route53_interface - INFO - Found record of type SOA with ttl 900 named example.com.
2021-09-02 22:09:19,437 - route53_ddns.route53_interface - INFO - Found record of type A with ttl 60 named pif.example.com.
2021-09-02 22:09:19,438 - route53_ddns.route53_interface - INFO - Found record of type A with ttl 60 named ppi.example.com.
2021-09-02 22:09:19,438 - route53_ddns.route53_interface - INFO - Found record of type A with ttl 60 named rpi.example.com.
2021-09-02 22:09:19,438 - route53_ddns.route53_interface - INFO - No records found matching home.example.com. A new 'A' record would be created.
2021-09-02 22:09:19,438 - route53_ddns.route53_interface - INFO - The current value of home.example.com points to None. Will update to 10.0.0.1
2021-09-02 22:09:19,438 - route53_ddns.route53_interface - INFO - Submitting the change for home.example.com to point to 10.0.0.1
2021-09-02 22:09:20,112 - route53_ddns.route53_interface - INFO - Status of change /change/C042853219OW934Y2B3A2 is still pending. Waiting 5 seconds
2021-09-02 22:09:25,556 - route53_ddns.route53_interface - INFO - Status of change /change/C042853219OW934Y2B3A2 is still pending. Waiting 5 seconds
2021-09-02 22:09:30,942 - route53_ddns.route53_interface - INFO - Status of change /change/C042853219OW934Y2B3A2 is still pending. Waiting 5 seconds
2021-09-02 22:09:36,155 - route53_ddns.route53_interface - INFO - Status of change /change/C042853219OW934Y2B3A2 is still pending. Waiting 5 seconds
2021-09-02 22:09:41,318 - route53_ddns.route53_interface - INFO - Status of change /change/C042853219OW934Y2B3A2 is still pending. Waiting 5 seconds
2021-09-02 22:09:46,619 - route53_ddns.route53_interface - INFO - Status of change /change/C042853219OW934Y2B3A2 is still pending. Waiting 5 seconds
2021-09-02 22:09:51,856 - route53_ddns.route53_interface - INFO - Change /change/C042853219OW934Y2B3A2 has completed with status INSYNC
2021-09-02 22:09:51,856 - route53_ddns.route53_interface - INFO - Update completed
2021-09-02 22:09:51,922 - route53_ddns.ip_utilities - INFO - Record home.example.com points to 10.0.0.1
```

To check the propagation status:

```bash
$ route53-ddns --zone example.com --record home -c
2021-09-02 22:14:43,791 - root - INFO - Adjusting target record to be home.example.com
2021-09-02 22:14:44,145 - route53_ddns.ip_utilities - INFO - Detected IP 10.0.0.1
2021-09-02 22:14:44,145 - root - INFO - Running in check-only mode. Validating propagation of 10.0.0.1
2021-09-02 22:14:44,146 - route53_ddns.ip_utilities - INFO - Record hom.example.com points to 10.0.0.1
```
