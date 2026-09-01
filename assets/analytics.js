/* VISUAL LABO 新橋店 — 計測タグ共通読み込み
   GA4の測定ID（G-から始まる）をここに入れると、全ページで計測が始まります。
   例: var GA4_ID = 'G-ABCD123XYZ';
   空のままなら何も読み込まれません（サイトの表示には影響しません）。 */
(function () {
  var GA4_ID = '';            // ← GA4の測定IDを入れる
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

    /* 予約・問い合わせボタンのクリックを計測（data-cta属性つきのリンク） */
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[data-cta]');
      if (a) gtag('event', 'cta_click', { cta: a.getAttribute('data-cta'), page: location.pathname });
    }, true);
  }

  if (CLARITY_ID) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }
})();
