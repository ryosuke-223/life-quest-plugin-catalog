# ローカル線プラグインのデータ出典

## 親プラグイン

`plugins/local-railways.json` は、経営会社別の子プラグインを選ぶための路線カタログです。子プラグインをインストールしていない路線も、路線名・経営会社名・手動の訪問状態だけを保持します。駅データを持たない路線は、対象路線の子プラグインを追加した時点で駅実績を同期します。

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
