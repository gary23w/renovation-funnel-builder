<?php
$is_ajax =
    "xmlhttprequest" === strtolower($_SERVER["HTTP_X_REQUESTED_WITH"] ?? "");
$hidden_field = $_POST["hidden_ninja"] ?? "";

// Basic validation to ensure the IP variable is not directly used from user input
$ip = filter_var($_SERVER["REMOTE_ADDR"], FILTER_VALIDATE_IP);
$rate_limit_file = "rate_limit/" . md5($ip) . ".txt"; // Securely creating a file name based on the user's IP
$limit = 5; // Limit of requests
$window = 60; // Time window in seconds

if ($is_ajax && empty($hidden_field)) {
    // Check rate limiting
    if (!is_dir("rate_limit")) {
        mkdir("rate_limit", 0700); // Ensure the rate_limit directory exists with proper permissions
    }

    $now = time();
    $allowed = true;

    if (file_exists($rate_limit_file)) {
        $data = json_decode(file_get_contents($rate_limit_file), true);
        $timestamp = $data["timestamp"] ?? $now;
        $count = $data["count"] ?? 0;

        if ($now - $timestamp < $window) {
            if ($count >= $limit) {
                $allowed = false;
            } else {
                $data["count"] = $count + 1;
            }
        } else {
            $data = ["timestamp" => $now, "count" => 1];
        }
    } else {
        $data = ["timestamp" => $now, "count" => 1];
    }

    if ($allowed) {
        file_put_contents($rate_limit_file, json_encode($data));

        // Continue processing form data
        $name = $_POST["name"] ?? "";
        $email = $_POST["email"] ?? "";
        $phone = $_POST["phone"] ?? "";
        $selection = $_POST["selection"] ?? "NO SELECTION";
        $message = $_POST["message"] ?? "NO MESSAGE";
        $ip = $_POST["ip"] ?? "";
        $hostname = $_POST["hostname"] ?? "";
        $region = $_POST["region"] ?? "";
        $country = $_POST["country"] ?? "";
        $loc = $_POST["loc"] ?? "";
        $org = $_POST["org"] ?? "";
        $postal = $_POST["postal"] ?? "";
        $timezone = $_POST["timezone"] ?? "";
        $page_url = $_POST["page_url"] ?? "";
        $dir = dirname(__FILE__);
        require $dir . "GarySendInBlue.php";
        $result = new GarySendInBlue(
            $name,
            $email,
            $phone,
            $selection,
            $message,
            1,
            $ip,
            $hostname,
            $region,
            $country,
            $loc,
            $org,
            $postal,
            $timezone,
            $page_url
        );
        $result = $result->Send();

        echo json_encode([
            "status" => "success",
            "message" => "Message sent successfully",
            "result" => $result,
        ]);
    } else {
        echo json_encode([
            "status" => "failed",
            "message" => "Rate limit exceeded. Please try again later.",
        ]);
    }
} else {
    echo json_encode([
        "status" => "failed",
        "message" =>
            "Oops, something went wrong. Either not AJAX or honeypot filled.",
    ]);
}

die();

?>