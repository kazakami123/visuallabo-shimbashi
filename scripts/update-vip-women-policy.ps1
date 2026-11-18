$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$files = Get-ChildItem -LiteralPath $repoRoot -Filter '*.html' -File
$files += Get-Item -LiteralPath (Join-Path $repoRoot 'tools\column-template.html')

$accessText = '男性専用・会員制の体型管理サロンです。女性のお客様は、VIP月額会員の男性ご本人が同伴し、完全個室のVIP ROOMを120分一緒に利用する場合に限り、単発＋10,000円（税込）でご案内します。女性単独での予約・来店はできません。'
$companionText = '女性のお連れ様は、VIP月額会員の男性ご本人が同伴し、完全個室のVIP ROOMを120分一緒に利用する場合に限り、単発＋10,000円（税込）でご案内します。女性単独での利用はできません。'
$womenPolicy = '女性は、VIP月額会員の男性ご本人が同伴し、完全個室のVIP ROOMを120分一緒に利用する場合に限り、単発＋10,000円（税込）でご利用いただけます。女性単独での予約・来店はできません。'
$womenReserve = '女性のお客様のご利用は、VIP月額会員の男性ご本人から事前にご予約ください。女性単独でのご予約は承っていません。'

foreach ($file in $files) {
    if ($file.Name -eq 'ladies.html') { continue }

    $content = [System.IO.File]::ReadAllText($file.FullName)
    $before = $content

    $content = [regex]::Replace(
        $content,
        '基本は男性専用です。月・火・水・金・土は男性専用のMEN''S DAY、木曜日は女性専用のLADIES DAY（2026年12月3日開始）、日曜日・祝日は男女共通のUNISEX DAY（.*?）として営業します。',
        $accessText
    )
    $content = [regex]::Replace(
        $content,
        '当サロンは男性専用の会員制体型管理サロンです。月・火・水・金・土は男性専用、木曜日は女性専用のLADIES DAY（2026年12月3日開始）、日曜日・祝日は男女共通のUNISEX DAY（.*?）として営業します。',
        $accessText
    )
    $content = $content.Replace('女性のお客様は、木曜日のLADIES DAY（女性専用）と日曜日・祝日のUNISEX DAY（男女共通）にご利用いただけます（ご予約は公式LINEのみ）。', '')
    $content = $content.Replace('がんばらない、体型管理習慣。新橋の、会員制体型管理サロン。木曜日はLADIES DAY（女性専用）。', 'がんばらない、体型管理習慣。新橋の男性専用・会員制体型管理サロン。女性はVIP月額会員の男性同伴・VIP ROOM限定。')
    $content = [regex]::Replace(
        $content,
        '施術のご利用は、その日の営業区分に沿ってご案内します（MEN''S DAY＝男性の方、LADIES DAY＝女性の方、UNISEX DAY＝男女どちらも）。お連れ様の同伴は男女どちらも承ります。',
        $companionText
    )
    $content = $content.Replace('女性のお客様も月額会員にご入会いただけます。', '女性単独での月額会員入会・ご利用は承っていません。')
    $content = $content.Replace('月額会員へのご入会は、女性のお客様も承っています。', '女性単独での月額会員入会・ご利用は承っていません。')
    $content = [regex]::Replace($content, '木曜日のLADIES DAY（女性専用・2026年12月3日から）と、日曜日・祝日のUNISEX DAY（男女共通）にご利用いただけます。2026年11月のUNISEX DAYは15日・22日・23日（祝）・29日です。', $womenPolicy)
    $content = [regex]::Replace($content, '木曜日のLADIES DAY（2026年12月3日開始）と、日曜日・祝日のUNISEX DAY（.*?）にご利用いただけます。.*?女性のお客様のご利用はお受けしておりません。', $womenPolicy)
    $content = $content.Replace('女性のお客様のご予約は、公式LINEのみで承ります。ホットペッパービューティー・お電話ではお受けしていません。ご希望の日時を2〜3候補お送りください。', $womenReserve)
    $content = $content.Replace('女性のお客様のご予約は、公式LINEのみで承ります。', $womenReserve)
    $content = [regex]::Replace($content, 'お腹まわり痩身体験 60分 ¥980（税込）をご用意しています。お一人さま1回。ご来店からお帰りまでの所要時間は約120分です。※ 効果・感じ方には個人差があります。1回で痩せることをお約束するものではありません。', '女性向けの単独初回体験はありません。VIP月額会員の男性同伴で、120分のVIP ROOM利用に単発＋10,000円（税込）で追加できます。')
    $content = $content.Replace('女性の初回体験 ¥980', 'VIP同伴 ＋¥10,000')
    $content = $content.Replace('お腹まわり痩身体験 60分 ¥980（税込）。ご予約は公式LINEのみで承ります。新橋駅 徒歩3分。', '女性はVIP月額会員の男性同伴・VIP ROOM限定。120分の同伴利用は単発＋10,000円（税込）です。')
    $content = [regex]::Replace($content, 'aria-label="公式LINEで初回体験を予約する。お腹まわり痩身体験60分、980円"><span><b class="br-full">公式LINEで予約する</b><b class="br-mini">LINEで予約</b></span><em>¥980</em>', 'aria-label="VIP会員の男性同伴利用を相談する。120分、追加10,000円"><span><b class="br-full">VIP同伴を相談する</b><b class="br-mini">同伴を相談</b></span><em>＋¥10,000</em>')

    if ($content -ne $before) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.UTF8Encoding]::new($false))
        Write-Output $file.Name
    }
}
