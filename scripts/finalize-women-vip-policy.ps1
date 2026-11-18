$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$files = Get-ChildItem -LiteralPath $repoRoot -Filter '*.html' -File
$policy = 'VISUAL LABO 新橋店は男性向けの会員制体型管理サロンです。女性は、VIP月額会員の男性ご本人が予約・来店・同伴し、同じVIP ROOMで120分を一緒に過ごす場合に限り、女性ゲスト1名をご案内します。女性同伴オプションは＋¥10,000（税込）です。女性単独の予約・来店・入会は承っていません。'
$policyShort = '女性はVIP月額会員の男性同伴・VIP ROOM限定です。女性ゲスト1名を、120分の同伴利用に単発＋¥10,000（税込）でご案内します。女性単独の予約・来店は承っていません。'

foreach ($file in $files) {
    if ($file.Name -eq 'ladies.html') { continue }

    $lines = [System.IO.File]::ReadAllLines($file.FullName)
    $changed = $false
    for ($i = 0; $i -lt $lines.Length; $i++) {
        $line = $lines[$i]

        if ($line -match 'LADIES DAY|UNISEX DAY') {
            if ($line -match '^\s*<!--') {
                $lines[$i] = '<!-- 女性のご利用はVIP月額会員の男性同伴・VIP ROOM限定です -->'
            } elseif ($line -match '"description"\s*:') {
                $lines[$i] = [regex]::Replace($line, '("description"\s*:\s*").*?("\s*,?\s*$)', '$1新橋駅徒歩3分の男性専用・会員制体型管理サロン。女性はVIP月額会員の男性同伴・VIP ROOM限定で、120分＋10,000円（税込）です。$2')
            } elseif ($line -match '"text"\s*:') {
                $lines[$i] = [regex]::Replace($line, '("text"\s*:\s*").*?("\s*}?)', ('$1' + $policy + '$2'))
            } elseif ($line -match '<details') {
                $indent = ($line -replace '^(\s*).*','$1')
                $summary = if ($line -match '<summary>(.*?)</summary>') { $Matches[1] } else { '女性も利用できますか？' }
                $lines[$i] = $indent + '<details><summary>' + $summary + '</summary><div class="a">' + $policy + '</div></details>'
            } elseif ($line -match '<div class="ic"') {
                $indent = ($line -replace '^(\s*).*','$1')
                $lines[$i] = $indent + '<div class="ic"><div class="lb">女性のご利用条件</div><div class="vl">VIP会員の男性同伴限定</div><small>女性ゲスト1名・VIP ROOM 120分・単発＋¥10,000（税込）。女性単独の予約・来店はできません。</small></div>'
            } elseif ($line -match '<div class="pcard"') {
                $indent = ($line -replace '^(\s*).*','$1')
                $lines[$i] = $indent + '<div class="pcard"><span class="n">01</span><h3>男性向け・完全個室</h3><p>' + $policyShort + '</p></div>'
            } elseif ($line -match '<dt>営業区分</dt>') {
                $indent = ($line -replace '^(\s*).*','$1')
                $lines[$i] = $indent + '<dt>女性のご利用</dt><dd>VIP月額会員の男性同伴・VIP ROOM限定<br>女性ゲスト1名／120分／＋¥10,000（税込）<br>女性単独の予約・来店は不可</dd>'
            } elseif ($line -match '<p') {
                $indent = ($line -replace '^(\s*).*','$1')
                $attrs = if ($line -match '<p([^>]*)>') { $Matches[1] } else { '' }
                $lines[$i] = $indent + '<p' + $attrs + '>' + $policyShort + '</p>'
            } elseif ($line -match '<li>') {
                $indent = ($line -replace '^(\s*).*','$1')
                $lines[$i] = $indent + '<li>' + $policy + '</li>'
            } elseif ($line -match '営業区分:') {
                $lines[$i] = '  女性の利用条件: VIP月額会員の男性同伴・VIP ROOM限定／女性ゲスト1名／120分／＋10,000円（税込）／女性単独利用不可'
            } else {
                $lines[$i] = $line -replace 'LADIES DAY（女性専用）|LADIES DAY|UNISEX DAY（男女共通）|UNISEX DAY', 'VIP同伴利用'
            }
            $changed = $true
            continue
        }

        if ($line -match '女性のお客様の初回体験|お腹まわり痩身体験 60分 ¥980|女性のお客様のご予約は.*公式LINE') {
            $indent = ($line -replace '^(\s*).*','$1')
            if ($line -match '<details') {
                $summary = if ($line -match '<summary>(.*?)</summary>') { $Matches[1] } else { '女性も利用できますか？' }
                $lines[$i] = $indent + '<details><summary>' + $summary + '</summary><div class="a">' + $policy + '</div></details>'
            } elseif ($line -match '"text"\s*:') {
                $lines[$i] = [regex]::Replace($line, '("text"\s*:\s*").*?("\s*}?)', ('$1' + $policy + '$2'))
            } elseif ($line -match '<div class="ic"') {
                $lines[$i] = $indent + '<div class="ic"><div class="lb">女性のご利用条件</div><div class="vl">VIP会員の男性同伴限定</div><small>女性ゲスト1名・VIP ROOM 120分・単発＋¥10,000（税込）。女性単独の予約・来店はできません。</small></div>'
            } elseif ($line -match '<p') {
                $attrs = if ($line -match '<p([^>]*)>') { $Matches[1] } else { '' }
                $lines[$i] = $indent + '<p' + $attrs + '>' + $policyShort + '</p>'
            } elseif ($line -match '<h2>') {
                $lines[$i] = $indent + '<h2>女性はVIP会員の男性同伴時のみご利用いただけます</h2>'
            } else {
                $lines[$i] = $line -replace '女性のお客様の初回体験', '女性のご利用条件'
            }
            $changed = $true
        }
    }

    if ($changed) {
        [System.IO.File]::WriteAllLines($file.FullName, $lines, [System.Text.UTF8Encoding]::new($false))
        Write-Output $file.Name
    }
}

# Page-specific cleanup after the legacy day-based copy has been removed.
$indexPath = Join-Path $repoRoot 'index.html'
$index = [System.IO.File]::ReadAllText($indexPath)
$indexSection = @'
<section class="sec" id="news-days" style="background:var(--wash);padding-top:clamp(36px,6vw,60px);padding-bottom:clamp(36px,6vw,60px)">
  <div class="wrap" style="max-width:780px">
    <div class="kicker c rv">VIP COMPANION ｜ 女性ゲストのご案内</div>
    <h2 class="rv" style="text-align:center;font-size:clamp(20px,3.4vw,27px);letter-spacing:.04em;line-height:1.7;margin:0 0 clamp(16px,3vw,24px)">大切な方と、同じVIP ROOMで過ごす120分。</h2>
    <div class="rv" style="background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:clamp(20px,4vw,30px)">
      <p style="font-size:14px;line-height:2.1;color:var(--ink-soft);margin:0 0 14px">女性のお客様は、<b style="color:var(--ink)">VIP月額会員の男性ご本人が予約・来店・同伴する場合のみ</b>ご利用いただけます。完全個室のVIP ROOMで、お二人一緒に120分お過ごしいただけます。</p>
      <p style="font-size:14px;line-height:2.1;color:var(--ink-soft);margin:0 0 14px"><b style="color:var(--ink)">女性ゲスト1名 ＋¥10,000（税込）</b>。VIP月額会員の通常利用へ、単発で追加できます。</p>
      <p style="font-size:14px;line-height:2.1;color:var(--ink-soft);margin:0">女性単独での予約・来店・入会は承っていません。女性向けのLADIES DAYは廃止しました。</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn btn-line" href="https://lin.ee/VAjIUgc" target="_blank" rel="noopener">VIP同伴利用を相談する</a><a class="btn btn-out" href="ladies.html">女性ゲストのご案内</a></div>
    </div>
  </div>
</section>
'@
$index = [regex]::Replace($index, '(?s)<section class="sec" id="news-days".*?</section>', $indexSection, 1)
$index = $index.Replace('木曜日のVIP同伴利用・日曜日・祝日のVIP同伴利用については<a href="#news-days" style="border-bottom:1px solid var(--gold-d)">営業体制のお知らせ</a>をご覧ください。', '女性ゲストはVIP月額会員の男性同伴・VIP ROOM限定でご案内します。')
[System.IO.File]::WriteAllText($indexPath, $index, [System.Text.UTF8Encoding]::new($false))

$flowPath = Join-Path $repoRoot 'flow.html'
$flow = [System.IO.File]::ReadAllText($flowPath)
$flow = [regex]::Replace($flow, '<div class="ic" id="flow-ladies">.*?</div>', '<div class="ic" id="flow-ladies"><div class="lb">女性のご利用条件</div><div class="vl">VIP会員の男性同伴限定</div><small>女性ゲスト1名・VIP ROOM 120分・単発＋¥10,000（税込）。女性単独利用不可。</small></div>')
$flow = $flow.Replace('<p>女性はVIP月額会員の男性同伴・VIP ROOM限定です。女性ゲスト1名を、120分の同伴利用に単発＋¥10,000（税込）でご案内します。女性単独の予約・来店は承っていません。</p>', '<div class="fstep"><div class="no">01</div><div><span class="tt">RESERVE</span><h3>ご予約</h3><p>女性ゲストのご利用は、VIP月額会員の男性ご本人から事前にご予約ください。女性ゲスト1名・VIP ROOM 120分・単発＋¥10,000（税込）です。女性単独の予約・来店は承っていません。</p></div></div>')
[System.IO.File]::WriteAllText($flowPath, $flow, [System.Text.UTF8Encoding]::new($false))

$newsPath = Join-Path $repoRoot 'news.html'
$news = [System.IO.File]::ReadAllText($newsPath)
$newsArticle = @'
  <article class="nws rv" id="news-20261118-vip-companion">
    <div class="nws-head"><time datetime="2026-11-18">2026.11.18</time><span class="nws-tag nws-tag-open">営業</span></div>
    <h2>女性のご利用は、VIP会員の男性同伴限定になりました</h2>
    <p>女性向けのLADIES DAYは廃止しました。現在、女性のお客様はVIP月額会員の男性ご本人が予約・来店・同伴し、完全個室のVIP ROOMを120分一緒に利用する場合のみご案内しています。</p>
    <p>女性ゲストは1名まで、通常のVIP利用に単発＋¥10,000（税込）で追加できます。女性単独での予約・来店・入会は承っていません。</p>
    <p class="nws-links"><a href="ladies.html">女性ゲストのご案内 →</a>　<a href="vip.html">VIP ROOMを見る →</a></p>
  </article>
'@
$news = [regex]::Replace($news, '(?s)\s*<article class="nws rv" id="news-20261110">.*?</article>\s*<article class="nws rv" id="news-20261110-ladies">.*?</article>', "`r`n$newsArticle", 1)
$news = $news.Replace('<p>日曜日はこれまでどおり<b>VIP同伴利用</b>です。男女どちらもご利用いただけます。営業時間は 10:00 — 18:00 です。</p>', '<p>女性のお客様は曜日を問わず、VIP月額会員の男性同伴・VIP ROOM限定でご案内します。</p>')
[System.IO.File]::WriteAllText($newsPath, $news, [System.Text.UTF8Encoding]::new($false))

# Retire three articles whose premise was the discontinued day-based women service.
$redirectPages = @('learn-ladies-hajimete.html','learn-ladies-kahanshin.html','learn-ladies-ninoude.html')
foreach ($name in $redirectPages) {
    $path = Join-Path $repoRoot $name
    $title = '女性ゲストのご案内｜VISUAL LABO 新橋店'
    $html = '<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + $title + '</title><meta name="description" content="女性はVIP月額会員の男性同伴・VIP ROOM限定。女性ゲスト1名、120分、＋10,000円（税込）でご利用いただけます。"><link rel="canonical" href="https://visuallabo.com/ladies.html"><meta http-equiv="refresh" content="0;url=ladies.html"><script>location.replace("ladies.html")</script></head><body><p><a href="ladies.html">女性ゲストの最新のご案内はこちら</a></p></body></html>'
    [System.IO.File]::WriteAllText($path, $html, [System.Text.UTF8Encoding]::new($false))
}
