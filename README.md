# canitconnect
## building
run the build.sh script to vendor dependancies
## cleaning
run the clean.sh script to remove vendored dependancies
## deploying
after building to vendor dependencies, simply `cf push` the included manifest is ample.


## Summary
Network tools running as CloudFoundry apps.
- python3
- cURL is implemented with urllib multiple methods to test
- Traceroute relys on the linux subsystem
- Show proxy related environmental vars
- Modiry proxy related environmental vars
- Grab system time
- REST API for our CLI happy people.... or machines.
- link to source

## Branding guide
Branding is done inside main.py
- indexComment => implement your own html comment <!-- your ascii art -->
- footerImg => base64 encoded image. Mine looks alright at 192 x 52 px
- headerImg => base64 encoded image. Mine looks alright at 60 x 60 px
- enterprise => The name of your corp, enterprise, or puppy

![](static/img/screenshot.png)

## Contributing
Write a test and submit your PR. I would be honored.
