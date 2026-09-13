# 日本の世界遺産めぐり：データ出典

確認日：2026-09-13

## 対象一覧

対象名、登録年、文化遺産・自然遺産の区分は、文化庁の[日本の世界遺産一覧](https://www.bunka.go.jp/seisaku/bunkazai/shokai/sekai_isan/ichiran/)を基準に整理しました。2026年登録の「飛鳥・藤原の宮都」を含む27件（文化遺産22件、自然遺産5件）です。新規登録と19構成資産は[UNESCO世界遺産委員会の決議](https://whc.unesco.org/en/decisions/9173/)でも照合しました。

文化庁の掲載内容をプラグイン用の項目に再構成し、出典を示しています。文化庁・文部科学省、環境省、自治体、UNESCOが本プラグインを作成または承認したことを示すものではありません。文部科学省サイトの利用条件は[文部科学省ウェブサイト利用規約](https://www.mext.go.jp/b_menu/1351168.htm)を参照してください。

## 位置情報と達成判定

プラグインには27件の遺産を親項目として登録し、合計251個の地点を持たせています。座標出典URLはプラグインの各地点の `sourceURL` に記録しました。

- 写真に保存されたGPS位置が、親項目のいずれかの判定地点に設定された範囲内なら、その世界遺産を1件達成します。同一遺産で複数地点に一致しても親項目・実績の件数は増えません。
- 標準の円判定半径は200mです。屋久島の黒味岳・宮之浦岳・本富岳、小笠原の中央山・乳房山、奄美大島等4地域の山頂、計9地点だけ300mにしています。これらは孤立した山岳地形に限った小さな余裕で、島全域や遺産区域全体を覆う半径ではありません。海上の船舶移動だけで解除される誤判定を避けるため、海域を含む地点は広げていません。
- 島しょ地域は公開代表地点を登録しています。小笠原諸島と奄美等は複数の島・地域に離れた地点を登録していますが、島内の登録区域を網羅する保証はありません。
- Wikidataから採用した地点は構造化座標（P625）を施設・地物名と照合し、QIDを `sourceURL` に記録しています。Wikidataの構造化データは[CC0](https://www.wikidata.org/wiki/Wikidata:Licensing)で公開されています。
- 公式座標が確認できる地点は、国土地理院の[山頂座標一覧](https://cyberjapandata.gsi.go.jp/3d/mountain/mountain.html)、環境省のGIS・登山ルート、自治体や施設管理者の公式地図・案内を優先しました。公式地図ピンの座標をデータ化した場合は、その地図または案内ページを地点の `sourceURL` に記録しています。
- 屋久島の候補は環境省の公式登山GISと[世界遺産区域GeoJSON](https://www.env.go.jp/park/yakushima/ywhcc/route/gis/heritage.geojson)を位置照合し、区域外の白谷雲水峡・弥生杉コース地点は除外しました。
- 白神山地は青森県公式観光ページのブナ林散策道地図ピンを使いました。林野庁は[散策道が遺産地域の緩衝地域内にある](https://www.rinya.maff.go.jp/tohoku/introduction/gaiyou_kyoku/annai/midokoro/midokoro_2017_12.html)と案内しています。管理計画ページにある核心地域・緩衝地域の面積の合計は16,971haで、[UNESCOの地理データ](https://whc.unesco.org/en/list/663/maps/)の登録資産面積と一致し、別個のUNESCO Buffer Zoneは掲載されていません。ルートは[白神山地ビジターセンター](https://www.shirakami-visitor.jp/sansaku_tozan/sansaku_buna.html)および[アクアグリーンビレッジANMON](https://www.anmon-shirakami.com/trekking/b2.html)で照合しました。
- 知床五湖の位置は[知床五湖の公式アクセス地図](https://www.goko.go.jp/access.html)を用いました。小笠原の中央山・乳房山および奄美等4地域の山頂位置は国土地理院の座標一覧を使い、遺産区域・歩道の説明を環境省や東京都の公式案内で照合しました。
- 宗像の沖ノ島本島は一般立入りが禁止されているためGPS地点を設けず、項目詳細に表示するだけで判定・達成数に含めません。[宗像大社の沖津宮案内](https://munakata-taisha.or.jp/about_okitsu.html)と[宗像市の沖津宮遙拝所案内](https://www.city.munakata.lg.jp/kanko/kiji0032577/index.html)に基づき、公開されている遙拝所・中津宮・辺津宮・古墳群のいずれか1地点で親項目を達成できる構成にしました。
- 紀伊山地の参詣道は、[和歌山県の公式ルート案内（中辺路・大辺路・高野参詣道）](https://www.wakayama-kanko.or.jp/courses/)、[奈良県の大峯奥駈道・小辺路資料](https://www.pref.nara.lg.jp/ikasu-nara/bunkashigen/)、三重県の[伊勢路・松本峠案内](https://www.kodo.pref.mie.lg.jp/navi/sp/routes/17_detail.html)をもとに、公式案内地点を採りました。石見銀山街道は[島根県の公式コース資料](https://www1.pref.shimane.lg.jp/tourism/nature/shimane/chugokusizenhodo/ginzan.html)で道筋と港・町並みを照合しました。

## 地図・境界データの再配布

- 国土交通省・国土数値情報の[世界文化遺産データ](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A34-v1_2.html)と[世界自然遺産データ](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A28.html)は利用条件が非商用です。国土数値情報の[利用規約](https://nlftp.mlit.go.jp/ksj/other/agreement_02.html)は非商用データの複製物再配布を認めず、[FAQ](https://nlftp.mlit.go.jp/ksj/other/faq.html)も非商用データをソフトウェア等に同梱して販売できないと説明しています。そのため、世界遺産境界のポリゴンは本カタログに複製していません。
- UNESCOの地図・空間データは同機関の[FAQ](https://whc.unesco.org/en/faq/126)に従い、許可が必要なデータを再掲載していません。屋久島の区域GeoJSONは照合にだけ使い、マニフェストやカタログへ境界形状を複製していません。
- iOSアプリの判定処理とカタログ検証器はGeoJSONの `Polygon` / `MultiPolygon` に対応済みです。したがって、将来は再配布条件が確認できる公式境界データが見つかった遺産に限ってポリゴン判定を追加できます。現状の円は登録区域を正確に示すものではありません。
- Wikidataを使った座標はCC0として公開された構造化データをもとにしています。政府・自治体ページの内容は、各サイトの利用条件に従い、名称・事実・地図ピン座標を必要な範囲で項目化しています。個々の位置は出典URLから再確認できます。
- 画像、地図タイル、UNESCOロゴやエンブレム、観光ページの写真はカタログに含めていません。

## 判定精度と現地利用

判定地点の標準半径は200mで、孤立した自然遺産の山頂9地点のみ300mです。円は写真GPSの誤差と地点の幅を考慮した訪問判定の目安であり、登録区域・構成資産の形状を正確に示す境界ではありません。自然遺産の山岳地点、広域地形、参詣道や銀山街道は代表地点のみで、全区域を判定するものではありません。

位置情報は訪問検出用であり、現地への立入りが可能であることを保証しません。島への船便、施設公開日、登山道の閉鎖、ガイド同伴や入山手続は更新されるため、出発前に出典ページと現地管理者の最新情報を確認してください。

地点数・座標方針・採用／除外理由の詳細は [WORLD_HERITAGE_COORDINATE_RESEARCH.md](WORLD_HERITAGE_COORDINATE_RESEARCH.md) に記載しています。
