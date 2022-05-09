
template45 = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#007CC7" style="padding: 40px 0 30px 0;">
        <img src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" alt="aiti logo" style="width:199px;height:69px;">
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
    <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
    </td>
    </tr>
        <tr>
            <td style="color: #153643; font-family: Roboto, sans-serif; font-size: 20px; line-height: 24px; padding: 20px 0 30px 0;">
       
                <h3> <p>Dear Supervisor,</p> </h3>

                        <p>Your appraisee  {firstname} {middlename} {lastname} has sent comments on workplan. Please review and add your comments by following the link..</p>

                        <p>Below are the scores and comment from your appraisee</p>
                        1. Core Competencies Assessment Score - {core_assessments}</br>
                        2. Non-Core Competencies Assessment Score - {non_core_assessments}</br>
                        3. Total Score - {overall_total}</br>
                        4. Overall Rating - {overall_performance_rating}</br>
                        5. Appraisee comments - {appraisees_comments_and_plan}</p></br>
                         <strong><p>Please follow the link to give your assessment .</strong></br>
                         
                    <a href={frontend_url}/login target="_blank">Add comments</a> </p>
                 

                        Thank You. <br/>
                        Performance Appraisal Admin
                    </p>


            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#007CC7" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" width="100%" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>


"""
