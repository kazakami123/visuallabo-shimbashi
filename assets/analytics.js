/* VISUAL LABO 新橋店 — 計測タグ共通読み込み
   GA4の測定ID（G-から始まる）をここに入れると、全ページで計測が始まります。
   例: var GA4_ID = 'G-ABCD123XYZ';
   空のままなら何も読み込まれません（サイトの表示には影響しません）。 */
(function () {
  var GA4_ID = 'G-G17GN7QY0N';  // ← GA4の測定ID
  var CLARITY_ID = '';        // ← Microsoft Clarity を使う場合のプロジェクトID（任意）

  if (GA4_ID) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA4_ID);

    /* 予約・問い合わせボタンのクリックを計測（data-cta属性つきのリンク）
       GA4では cta（ボタンの場所）と channel（導線の種類）で分けて見られる。
       channel は遷移先から自動で判定するので、HTML側の追加は要らない。
       ここで取れるのは「予約ボタンを押した」までで、予約完了ではない点に注意。
       予約はLINE／ホットペッパー／電話という外部で完了するため、
       完了数は各サービス側の数字と突き合わせる（2026-10-05） */
    var channelOf = function (href, cta) {
      if (!href) return 'other';
      if (href.indexOf('tel:') === 0) return 'tel';
      if (href.indexOf('lin.ee') > -1 || href.indexOf('line.me') > -1) return 'line';
      if (href.indexOf('b.hpr.jp') > -1 || href.indexOf('beauty.hotpepper.jp') > -1) return 'hpb';
      if (/^https?:/.test(href) && href.indexOf(location.hostname) === -1) return 'external';
      return 'internal';
    };
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[data-cta]');
      if (!a) return;
      var cta = a.getAttribute('data-cta') || '';
      gtag('event', 'cta_click', {
        cta: cta,
        channel: channelOf(a.getAttribute('href'), cta),
        page: location.pathname
      });
    }, true);
  }

  /* ヘッダーのナビが入りきらないときだけ、右端をぼかして続きがあることを示す。
     項目を隠すのをやめて横スクロールにしたため（2026-09-23）。
     全ページがこのファイルを読み込んでいるので、ここに置いている */
  (function () {
    var nav = document.querySelector('.navlinks');
    if (!nav) return;
    var sync = function () {
      nav.classList.toggle('is-scrollable', nav.scrollWidth > nav.clientWidth + 1);
    };
    sync();
    window.addEventListener('resize', sync, { passive: true });
    window.addEventListener('load', sync);
  })();

  if (CLARITY_ID) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }
})();
