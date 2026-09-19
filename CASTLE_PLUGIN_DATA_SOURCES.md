# 名城・城跡コレクション：データ出典と判定範囲

データ確認日：2026-09-13

## 対象範囲

日本各地から選んだ27か所を記録する非公式コレクションです。全国の城を網羅する一覧、公式認定、スタンプラリーではありません。

## 名称・代表座標

各城の項目名は一般的な表記・別称を含みます。代表座標はWikidataの各項目の地理座標（P625）を照合して設定しました。代表座標は城郭敷地の境界を表すものではなく、敷地範囲の照合には次節の別データを用います。27件の座標は調査時点で該当項目のP625と一致しました。

Wikidataの構造化データは[Wikidata Licensing](https://www.wikidata.org/wiki/Wikidata:Licensing)に従いCC0として扱います。

| ID | 城郭 | Wikidata | 判定範囲 |
| --- | --- | --- | --- |
| `goryokaku` | 五稜郭 | [Q1196357](https://www.wikidata.org/wiki/Q1196357) | OSMの五稜郭ポリゴン |
| `matsumae` | 松前城 | [Q1143974](https://www.wikidata.org/wiki/Q1143974) | OSMの松前公園ポリゴン |
| `hirosaki` | 弘前城 | [Q328582](https://www.wikidata.org/wiki/Q328582) | OSMの弘前公園ポリゴン |
| `morioka` | 盛岡城 | [Q251650](https://www.wikidata.org/wiki/Q251650) | OSMの岩手公園ポリゴン |
| `sendai` | 仙台城跡（青葉城） | [Q598621](https://www.wikidata.org/wiki/Q598621) | 代表地点から半径250m |
| `aizu-wakamatsu` | 会津若松城（鶴ヶ城） | [Q1365061](https://www.wikidata.org/wiki/Q1365061) | OSMの鶴ヶ城公園ポリゴン |
| `odawara` | 小田原城 | [Q1013437](https://www.wikidata.org/wiki/Q1013437) | OSMの小田原城址公園ポリゴン |
| `kawagoe` | 川越城 | [Q1073688](https://www.wikidata.org/wiki/Q1073688) | 代表地点から半径250m |
| `sakura` | 佐倉城跡 | [Q8014937](https://www.wikidata.org/wiki/Q8014937) | OSMの佐倉城址公園ポリゴン |
| `hachioji` | 八王子城跡 | [Q2969389](https://www.wikidata.org/wiki/Q2969389) | 代表地点から半径250m |
| `matsumoto` | 松本城 | [Q739612](https://www.wikidata.org/wiki/Q739612) | OSMの松本城公園ポリゴン |
| `kanazawa` | 金沢城 | [Q511412](https://www.wikidata.org/wiki/Q511412) | OSMの金沢城公園ポリゴン |
| `inuyama` | 犬山城 | [Q1155484](https://www.wikidata.org/wiki/Q1155484) | 代表地点から半径250m |
| `nagoya` | 名古屋城 | [Q648629](https://www.wikidata.org/wiki/Q648629) | OSMの名古屋城ポリゴン |
| `iwamura` | 岩村城跡 | [Q1196356](https://www.wikidata.org/wiki/Q1196356) | 代表地点から半径250m |
| `hikone` | 彦根城 | [Q1012374](https://www.wikidata.org/wiki/Q1012374) | OSMの彦根城ポリゴン |
| `nijo` | 二条城 | [Q1013399](https://www.wikidata.org/wiki/Q1013399) | OSMの二条城ポリゴン |
| `osaka` | 大阪城 | [Q102178360](https://www.wikidata.org/wiki/Q102178360) | OSMの大阪城公園ポリゴン |
| `himeji` | 姫路城 | [Q188754](https://www.wikidata.org/wiki/Q188754) | OSMの姫路公園マルチポリゴン |
| `takeda` | 竹田城跡 | [Q8013060](https://www.wikidata.org/wiki/Q8013060) | 代表地点から半径250m |
| `matsue` | 松江城 | [Q151776](https://www.wikidata.org/wiki/Q151776) | OSMの松江城山公園ポリゴン |
| `okayama` | 岡山城 | [Q1013448](https://www.wikidata.org/wiki/Q1013448) | OSMの烏城公園ポリゴン |
| `marugame` | 丸亀城 | [Q250658](https://www.wikidata.org/wiki/Q250658) | 代表地点から半径250m |
| `kochi` | 高知城 | [Q1012815](https://www.wikidata.org/wiki/Q1012815) | 代表地点から半径250m |
| `kumamoto` | 熊本城 | [Q613355](https://www.wikidata.org/wiki/Q613355) | OSMの熊本城ポリゴン |
| `shuri` | 首里城 | [Q907052](https://www.wikidata.org/wiki/Q907052) | OSMの首里城公園ポリゴン |
| `nakagusuku` | 中城城跡 | [Q1013209](https://www.wikidata.org/wiki/Q1013209) | OSMの中城城跡ポリゴン |

## 判定範囲の形状とライセンス

19件は、代表座標を含むOpenStreetMap（OSM）の城郭・城址公園の地物をGeoJSONとして登録しました。各オブジェクトの形状は2026-09-13に取得・確認しています。

| 城郭 | OSMオブジェクト | GeoJSON |
| --- | --- | --- |
| 五稜郭 | [way/180806137](https://www.openstreetmap.org/way/180806137) | Polygon |
| 松前城 | [way/488836871](https://www.openstreetmap.org/way/488836871) | Polygon |
| 弘前城 | [way/85932862](https://www.openstreetmap.org/way/85932862) | Polygon |
| 盛岡城 | [way/51481168](https://www.openstreetmap.org/way/51481168) | Polygon |
| 会津若松城 | [way/36809202](https://www.openstreetmap.org/way/36809202) | Polygon |
| 小田原城 | [way/232722951](https://www.openstreetmap.org/way/232722951) | Polygon |
| 佐倉城跡 | [way/693873811](https://www.openstreetmap.org/way/693873811) | Polygon |
| 松本城 | [way/553388940](https://www.openstreetmap.org/way/553388940) | Polygon |
| 金沢城 | [way/128905245](https://www.openstreetmap.org/way/128905245) | Polygon |
| 名古屋城 | [relation/19100633](https://www.openstreetmap.org/relation/19100633) | Polygon |
| 彦根城 | [way/209262408](https://www.openstreetmap.org/way/209262408) | Polygon |
| 二条城 | [way/57111281](https://www.openstreetmap.org/way/57111281) | Polygon |
| 大阪城 | [way/35457792](https://www.openstreetmap.org/way/35457792) | Polygon |
| 姫路城 | [relation/3743076](https://www.openstreetmap.org/relation/3743076) | MultiPolygon |
| 松江城 | [way/52612698](https://www.openstreetmap.org/way/52612698) | Polygon |
| 岡山城 | [way/96200691](https://www.openstreetmap.org/way/96200691) | Polygon |
| 熊本城 | [way/375062710](https://www.openstreetmap.org/way/375062710) | Polygon |
| 首里城 | [way/380509890](https://www.openstreetmap.org/way/380509890) | Polygon |
| 中城城跡 | [way/218650220](https://www.openstreetmap.org/way/218650220) | Polygon |

OSMの地物はコミュニティ編集の地図データです。公園ポリゴンが外濠や文化財指定範囲と一致するとは限らず、公式な敷地境界として扱っていません。代表座標がポリゴン内にあることは確認しましたが、これらは城跡周辺を含む広い訪問範囲の近似です。データの再利用条件は[OpenStreetMapの著作権・ライセンス](https://www.openstreetmap.org/copyright)に従い、ODbL 1.0とします。プラグインの地図下に帰属表示を出し、個々の地点に `sourceURL` は持たせません。

敷地規模のポリゴンを確認できなかった仙台城跡、川越城、八王子城跡、犬山城、岩村城跡、竹田城跡、丸亀城、高知城の8件は、Wikidataの代表座標から半径250mの円を維持します。この円は敷地境界ではなく、敷地外の写真位置を拾う可能性があります。根拠のない範囲拡大は行わず、適切な境界データを確認できた時点で更新します。

## 写真位置による判定

アプリは写真の撮影時に記録された位置を照合します。ポリゴン内（穴の内側と穴の境界を除く）または円の半径内の撮影位置があれば、その城を「推定」として記録します。写真に写った対象物や撮影方向は画像認識しません。そのため、城を遠くから撮影して撮影者の位置が登録範囲外だった場合は自動判定されず、必要に応じてアプリ上で手動修正できます。

## 更新方針

名称・代表座標を変更するときは該当Wikidata項目とP625を再確認します。境界を変更するときはOSMオブジェクトID、形状、代表座標が内側にあること、穴の扱いを確認し、確認日を更新します。敷地・外濠を正確に表す公的な境界資料が確認できた場合は、近似ポリゴンや円より優先します。
