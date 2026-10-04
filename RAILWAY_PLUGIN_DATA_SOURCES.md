# ローカル線プラグインのデータ出典

## 親プラグイン

`plugins/local-railways.json` は、経営会社別の子プラグインを選ぶための路線カタログです。子プラグインをインストールしていない路線も、路線名・経営会社名・手動の訪問状態だけを保持します。駅データを持たない路線は、対象路線の子プラグインを追加した時点で駅実績を同期します。

子プラグインは経営会社ごとに1件作成し、駅を項目、路線をグループとして登録します。子プラグインを追加・更新するときは、同じ変更で親に次の3点を登録します。

1. 経営会社の `groups` エントリ
2. その会社が運営する全路線の `items` エントリ
3. 各路線グループと親路線を結ぶ `collection.routeLinks`

カタログ検証は、子プラグインの全路線グループが親へリンクされていること、リンク先の親路線が存在すること、同じ子プラグインのリンク先が同じ経営会社グループであることを確認します。子プラグイン未提供の路線は、親に登録して手動訪問だけを使えます。

## 三陸鉄道 リアス線

`plugins/railway-sanriku.json` の駅名と全41駅の並びは、三陸鉄道公式「路線・駅紹介」を確認して作成しました。

- 公式駅一覧: https://www.sanrikutetsudou.com/路線・駅紹介/
- 公式サイトの取得確認日: 2026-09-28
- 全41駅で、リアス線の各駅を1項目として登録しています。新田老駅（2020年開業）と八木沢・宮古短大駅、払川駅を含みます。

駅座標は、駅中心付近の公開座標を採用し、アプリの `photoLocation` 判定半径を一律100mとしています。駅中心から100mという判定方針は、駅構内・駅前で撮影した写真を対象にし、路線沿線全体を駅訪問と誤判定しないためのものです。座標の照合には次の公開データを使いました。

- 国土地理協会の全国沿線・駅データベースの説明（OpenStreetMap座標と国土地理院の換算方法）: https://www.kokudo.or.jp/database/004.html
- 全国の鉄道旅客駅リスト（駅名・緯度経度の照合）: https://www.desktoptetsu.com/quiz/all-stations.htm
- 鉄道駅データの公開一覧（旧駅名・駅中心座標の補助照合）: https://gist.github.com/ak0-hal-ns/3cf38e10c96a74f7cf4f035b6e4d2775
- 新田老駅の座標・開業情報の補助照合: https://www.wikidata.org/wiki/Q55525813
- 八木沢・宮古短大駅の座標・開業情報の補助照合: https://www.wikidata.org/wiki/Q55525757

座標データの地図表示には OpenStreetMap の帰属表示を付けています。座標の再利用条件は [OpenStreetMap Copyright](https://www.openstreetmap.org/copyright) と ODbL 1.0 に従います。公開ページの更新や駅位置の変更があった場合は、公式駅一覧を再確認してプラグインのバージョンを上げます。

## 東京メトロ

`plugins/railway-tokyo-metro.json` は、東京メトロ9路線を路線別の駅グループとして登録しています。

- 公式路線・駅一覧: https://www.tokyometro.jp/station/index.html
- 公式路線別駅一覧（駅数・駅順の照合）: https://www.tokyometro.jp/tcn/route_station/index.html
- 公式営業状況（全体の駅数180駅、9路線の営業区間）: https://www.tokyometro.jp/corporate/enterprise/passenger_rail/transportation/lines/index.html
- 公式サイトの取得確認日: 2026-10-04

公式路線別一覧の駅数は、銀座線19、丸ノ内線28、日比谷線22、東西線23、千代田線20、有楽町線24、半蔵門線14、南北線19、副都心線16です。乗換駅は路線ごとの実績を正しく集計するため、同じ物理駅でも路線別の項目として登録し、合計185項目にしています。東京メトロが会社情報で示す180駅は、乗換駅を駅施設として重複計上しない数え方です。

駅中心の座標は、MIT Licenseで公開されている `select766/tokyo-train-time-map` の `data/station_locations.csv`（取得確認日: 2026-10-04）を使用しました。

- データリポジトリ: https://github.com/select766/tokyo-train-time-map
- 座標CSV: https://raw.githubusercontent.com/select766/tokyo-train-time-map/master/data/station_locations.csv
- ライセンス: MIT License（リポジトリのLICENSEに記載）

すべての駅項目に `photoLocation` と `radiusMeters: 100` を設定しています。地下駅では地上出入口や駅中心の位置と写真のGPSがずれる可能性があるため、誤判定がある場合は手動訪問状態で補正できます。駅名・路線構成の更新や新駅開業があった場合は、公式一覧と座標データを再確認してプラグインのバージョンを上げます。
