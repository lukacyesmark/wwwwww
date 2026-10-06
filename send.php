<?php
/**
 * wwwwww.cz — odeslání poptávkového formuláře na e-mail.
 * Funguje s fetch() (vrací JSON) i bez JavaScriptu (přesměruje zpět s ?odeslano=1).
 */
declare(strict_types=1);

const RECIPIENT = 'lukac@yesmark.eu';
const FROM      = 'web@wwwwww.cz';   // adresa na doméně webu — kvůli SPF/DMARC doručitelnosti

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function respond(bool $ok, string $error = ''): void {
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($ok ? 200 : 400);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'error' => $error]);
    } else {
        $back = parse_url($_SERVER['HTTP_REFERER'] ?? '/', PHP_URL_PATH) ?: '/';
        header('Location: ' . $back . ($ok ? '?odeslano=1#poptavka' : '?chyba=1#poptavka'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST', true, 405);
    exit;
}

$clean = static fn(string $k, int $max = 500): string =>
    trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max));

// Antispam: honeypot + příliš rychlé odeslání
if ($clean('website') !== '') respond(true);           // bot — tvaříme se, že prošlo
if ((int)$clean('ts', 10) > 0 && (int)$clean('ts', 10) < 3) respond(true);

$name     = preg_replace('/[\n\t]+/', ' ', $clean('name', 120));
$email    = $clean('email', 160);
$phone    = preg_replace('/[^\d+ ()-]/', '', $clean('phone', 40));
$message  = $clean('message', 5000);
$page     = $clean('page', 40);
$attr     = $clean('attribution', 600);
$interest = array_map(
    static fn($v) => mb_substr(preg_replace('/[\r\n]+/', ' ', (string)$v), 0, 40),
    array_slice((array)($_POST['interest'] ?? []), 0, 10)
);

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'invalid');
}

$subject = 'Poptávka z wwwwww.cz — ' . $name;
$body = implode("\n", [
    "Nová poptávka z webu wwwwww.cz",
    str_repeat('-', 40),
    "Jméno:    $name",
    "E-mail:   $email",
    "Telefon:  " . ($phone ?: '—'),
    "Zájem o:  " . ($interest ? implode(', ', $interest) : '—'),
    "Stránka:  $page",
    "",
    "Zpráva:",
    $message,
    "",
    str_repeat('-', 40),
    "Zdroj:    $attr",
    "IP:       " . ($_SERVER['REMOTE_ADDR'] ?? ''),
    "Čas:      " . date('j. n. Y H:i'),
]);

$headers = implode("\r\n", [
    'From: =?UTF-8?B?' . base64_encode('wwwwww.cz') . '?= <' . FROM . '>',
    'Reply-To: =?UTF-8?B?' . base64_encode($name) . '?= <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: wwwwww.cz',
]);

$sent = mail(RECIPIENT, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . FROM);
respond($sent, $sent ? '' : 'mail');
