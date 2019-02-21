```bash
mkdir nginx_test
cd nginx_test
git clone https://github.com/ivarin/nginx_sandbox.git .
pytest tests/test_nginx.py --junitxml=./report.xml --name terraform-example-elb-40329900.us-west-2.elb.amazonaws.com --address 35.166.255.188 -s
```