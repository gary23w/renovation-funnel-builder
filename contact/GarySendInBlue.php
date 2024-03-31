<?php
class GarySendInBlue
{
    private $maillist = ["YOUR@EMAIL.HERE"]; // test

    //determine spam in the mailserver with AI
    function __construct(
        string $name,
        string $email,
        string $phone,
        string $selection,
        string $message,
        int $type,
        string $ip,
        string $hostname,
        string $region,
        string $country,
        string $loc,
        string $org,
        string $postal,
        string $timezone,
        string $page_url
    ) {
        $this->DestinationEmail = $email;
        $this->DestinationName = $name;
        $this->DestinationPhone = $phone;
        $this->DestinationSelection = $selection;
        $this->DestinationMessage = $message;
        $this->Type = $type;
        $this->IP = $ip;
        $this->Hostname = $hostname;
        $this->Region = $region;
        $this->Country = $country;
        $this->Loc = $loc;
        $this->Org = $org;
        $this->Postal = $postal;
        $this->Timezone = $timezone;
        $this->PageUrl = $page_url;
    }

    private function SetHeaders()
    {
        $headers = [];
        $headers[] = "Accept: application/json";
        $headers[] = "Api-Key: YOUR-KEY-HERE";
        $headers[] = "Content-Type: application/json";
        return $headers;
    }

    private function SetBody()
    {
        $body = [];
        $body["sender"] = [
            "name" => "donotreply@gary.ca",
            "email" => "donotreply@gary.ca",
        ];
        $body["to"] = [
            [
                "email" => "",
                "name" => "lead-gen",
            ],
        ];
        //get time
        $date = date("Y-m-d H:i:s");
        $body["subject"] = "new lead " . $date;
        $body["htmlContent"] =
            '
<html>
<head></head>
<body>
<h1>You have a lead.</h1>
<p>Name: ' .
            $this->DestinationName .
            '</p>
<hr />
<p>Email: ' .
            $this->DestinationEmail .
            '</p>
<hr />
<p>Phone: ' .
            $this->DestinationPhone .
            '</p>
<hr />
<p>Selection: ' .
            $this->DestinationSelection .
            '</p>
<hr />
<p>Message: ' .
            $this->DestinationMessage .
            '</p>
<hr />
<p>Time: ' .
            $date .
            '</p>
<hr />
<p>Type: ' .
            $this->Type .
            '</p>
<hr />
<p>IP: ' .
            $this->IP .
            '</p>
<hr />
<p>Hostname: ' .
            $this->Hostname .
            '</p>
<hr />
<p>Region: ' .
            $this->Region .
            '</p>
<hr />
<p>Country: ' .
            $this->Country .
            '</p>
<hr />
<p>Loc: ' .
            $this->Loc .
            '</p>
<hr />
<p>Org: ' .
            $this->Org .
            '</p>
<hr />
<p>Postal: ' .
            $this->Postal .
            '</p>
<hr />
<p>Timezone: ' .
            $this->Timezone .
            '</p>
<hr />
<p>Page URL: ' .
            $this->PageUrl .
            '</p>
</body></html>
';
        return $body;
    }

    public function Send()
    {
        $code = [];
        foreach ($this->maillist as $user) {
            $body = $this->SetBody();
            $body["to"][0]["email"] = $user;
            $headers = $this->SetHeaders();
            $ch = curl_init();
            curl_setopt(
                $ch,
                CURLOPT_URL,
                "https://api.brevo.com/v3/smtp/email"
            );
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $server_output = curl_exec($ch);
            curl_close($ch);
            $result = json_decode($server_output, true);
            $code[] = $result;
        }
        return $code;
    }
}