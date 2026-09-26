# 博物館・美術館めぐり：データ出典と判定範囲

確認日：2026-09-27

## 対象範囲

`japan-museums-art` は、日本各地の代表的な博物館・美術館を訪問図鑑として記録する非公式コレクションです。全国の博物館・美術館を網羅する一覧、文化庁の指定名簿、スタンプラリーの公式リストではありません。

地域の偏りを抑え、総合博物館、科学博物館、歴史博物館、近現代美術館、国立館、地方館、直島のアート施設を含めた28館を選びました。館種は実績の説明に使うための編集上の分類で、各館の正式な設置区分を変更するものではありません。

## 名称・座標・公式案内

名称と館種は、各館の公式案内ページで確認しました。位置判定に使う代表座標は、下表のWikidata項目に登録された地理座標（P625）を取得し、2026-09-27に項目名・座標を照合しました。Wikidataの構造化データは[CC0](https://www.wikidata.org/wiki/Wikidata:Licensing)として公開されています。

| ID | 館名 | 館種 | Wikidata | 代表座標（緯度, 経度） | 公式案内 |
| --- | --- | --- | --- | --- | --- |
| `hokkaido-museum` | 北海道博物館 | 博物館 | [Q11403709](https://www.wikidata.org/wiki/Q11403709) | 43.053000, 141.496611 | [公式](https://www.hm.pref.hokkaido.lg.jp/) |
| `hokkaido-modern-art` | 北海道立近代美術館 | 美術館 | [Q11402992](https://www.wikidata.org/wiki/Q11402992) | 43.060278, 141.330389 | [公式](https://www.dokyoi.pref.hokkaido.lg.jp/hk/knb/) |
| `aomori-art` | 青森県立美術館 | 美術館 | [Q11662266](https://www.wikidata.org/wiki/Q11662266) | 40.807300, 140.701000 | [公式](https://www.aomori-museum.jp/) |
| `iwate-art` | 岩手県立美術館 | 美術館 | [Q3298581](https://www.wikidata.org/wiki/Q3298581) | 39.693500, 141.124889 | [公式](https://www.ima.or.jp/) |
| `sendai-city-museum` | 仙台市博物館 | 博物館 | [Q3330092](https://www.wikidata.org/wiki/Q3330092) | 38.256065, 140.856685 | [公式](https://www.city.sendai.jp/museum/) |
| `tokyo-national-museum` | 東京国立博物館 | 博物館 | [Q653433](https://www.wikidata.org/wiki/Q653433) | 35.718889, 139.776389 | [公式](https://www.tnm.jp/) |
| `national-science-museum` | 国立科学博物館 | 博物館 | [Q74940](https://www.wikidata.org/wiki/Q74940) | 35.716319, 139.776544 | [公式](https://www.kahaku.go.jp/) |
| `momat` | 東京国立近代美術館 | 美術館 | [Q1359908](https://www.wikidata.org/wiki/Q1359908) | 35.690553, 139.754642 | [公式](https://www.momat.go.jp/) |
| `national-western-art` | 国立西洋美術館 | 美術館 | [Q1362629](https://www.wikidata.org/wiki/Q1362629) | 35.715357, 139.775850 | [公式](https://www.nmwa.go.jp/jp/) |
| `national-art-center-tokyo` | 国立新美術館 | 美術館 | [Q1362638](https://www.wikidata.org/wiki/Q1362638) | 35.665280, 139.726340 | [公式](https://www.nact.jp/) |
| `yokohama-art` | 横浜美術館 | 美術館 | [Q861588](https://www.wikidata.org/wiki/Q861588) | 35.457100, 139.631000 | [公式](https://yokohama.art.museum/) |
| `kanazawa-21c` | 金沢21世紀美術館 | 美術館 | [Q3242206](https://www.wikidata.org/wiki/Q3242206) | 36.560800, 136.658000 | [公式](https://www.kanazawa21.jp/) |
| `toyama-art` | 富山県美術館 | 美術館 | [Q28689689](https://www.wikidata.org/wiki/Q28689689) | 36.710556, 137.210000 | [公式](https://tad-toyama.jp/) |
| `tokugawa-art` | 徳川美術館 | 美術館 | [Q3077236](https://www.wikidata.org/wiki/Q3077236) | 35.183692, 136.933189 | [公式](https://www.tokugawa-art-museum.jp/) |
| `kyoto-national-museum` | 京都国立博物館 | 博物館 | [Q147286](https://www.wikidata.org/wiki/Q147286) | 34.989993, 135.773121 | [公式](https://www.kyohaku.go.jp/) |
| `kyoto-kyocera-art` | 京都市京セラ美術館 | 美術館 | [Q3330657](https://www.wikidata.org/wiki/Q3330657) | 35.012836, 135.783569 | [公式](https://kyotocity-kyocera.museum/) |
| `nara-national-museum` | 奈良国立博物館 | 博物館 | [Q147312](https://www.wikidata.org/wiki/Q147312) | 34.683700, 135.836400 | [公式](https://www.narahaku.go.jp/) |
| `national-art-museum-osaka` | 国立国際美術館 | 美術館 | [Q1055037](https://www.wikidata.org/wiki/Q1055037) | 34.691786, 135.492024 | [公式](https://www.nmao.go.jp/) |
| `osaka-history-museum` | 大阪歴史博物館 | 博物館 | [Q11261312](https://www.wikidata.org/wiki/Q11261312) | 34.682722, 135.520806 | [公式](https://www.osakamushis.jp/) |
| `ohara-art` | 大原美術館 | 美術館 | [Q2977589](https://www.wikidata.org/wiki/Q2977589) | 34.596150, 133.770670 | [公式](https://www.ohara.or.jp/) |
| `hiroshima-pref-art` | 広島県立美術館 | 美術館 | [Q3330773](https://www.wikidata.org/wiki/Q3330773) | 34.399908, 132.466275 | [公式](https://www.hpam.jp/) |
| `adachi-art` | 足立美術館 | 美術館 | [Q3329561](https://www.wikidata.org/wiki/Q3329561) | 35.380010, 133.194170 | [公式](https://www.adachi-museum.or.jp/) |
| `chichu-art` | 地中美術館 | 美術館 | [Q4556499](https://www.wikidata.org/wiki/Q4556499) | 34.449758, 133.985803 | [公式](https://benesse-artsite.jp/art/chichu.html) |
| `benesse-house` | ベネッセハウス ミュージアム | 美術館 | [Q131630258](https://www.wikidata.org/wiki/Q131630258) | 34.445254, 133.990815 | [公式](https://benesse-artsite.jp/art/benessehouse-museum.html) |
| `kyushu-national-museum` | 九州国立博物館 | 博物館 | [Q148543](https://www.wikidata.org/wiki/Q148543) | 33.518356, 130.538297 | [公式](https://www.kyuhaku.jp/) |
| `fukuoka-asian-art` | 福岡アジア美術館 | 美術館 | [Q3330163](https://www.wikidata.org/wiki/Q3330163) | 33.595028, 130.405917 | [公式](https://faam.city.fukuoka.lg.jp/) |
| `nagasaki-art` | 長崎県美術館 | 美術館 | [Q11652770](https://www.wikidata.org/wiki/Q11652770) | 32.741679, 129.871057 | [公式](https://www.nagasaki-museum.jp/) |
| `okinawa-pref-museum-art` | 沖縄県立博物館・美術館 | 博物館・美術館 | [Q4617100](https://www.wikidata.org/wiki/Q4617100) | 26.226593, 127.694103 | [公式](https://okimu.jp/) |

Wikidataのラベルが旧称になっている項目は、公式案内の現行名称をマニフェストに採用しました。たとえばQ3330657は旧称の「京都市美術館」を含む項目ですが、公式サイトの現行名称「京都市京セラ美術館」に合わせています。

## 写真位置による判定

各館の代表座標から**半径300m**を判定範囲にします。これは建物の正確な敷地境界ではなく、入口・周辺広場・GPS誤差を含む写真位置の近似です。隣接道路や別施設からの写真が訪問候補になる可能性があるため、自動判定は「推定」として扱い、必要に応じてLife Quest上で手動修正できます。

写真に位置情報がない場合、またはGPS誤差が大きい場合は自動判定されません。開館日、展示替え、予約、入場制限、撮影可否は変わるため、訪問前に各館の公式案内を確認してください。このプラグインは営業状態や入場資格を判定しません。

## 更新方針

館名・館種・公式URL・座標を変更するときは、該当館の公式案内とWikidataのP625を再確認し、確認日を更新します。閉館・移転・長期休館が判明した場合は、項目を削除せず、`detail` と出典資料に状態を記録したうえで次のバージョンで更新します。
