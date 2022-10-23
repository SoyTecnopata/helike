# HACKATON VERIFICATION MAIL TEST

To deploy  the lambda, chalice has to be install in a virtual enviroment on python and can be deploy by calling `deploy_hackaton_ses_test.sh`

To send a verification code, an the mail has to accept to be identify by
amazon in this [link]{https://us-east-1.console.aws.amazon.com/ses/home?region=us-east-1#/verified-identities}. It is need to be created an idenity  email address and after it is sent, we can spam the email with verification codes.

Currently, 2 endpoints can be used:

- `/send_verification_id` : To send a previous verified email a 6 digits code.

- `/confirm_verification_id` : If the code is the same one on s3 on the customer file, a `'true'` text is return to continue with the flow.
