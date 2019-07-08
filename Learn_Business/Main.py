from Reader.XMLreader import XMLreader


# inputデータ解析

# １。ファイル読み込み（input, file path. return ファイルの中身全部）


rpath = r"X:\Projects\test.xml"

reader = XMLreader(rpath)

for line in reader.lines:
    print(line)

# ２。無駄な要素を排除
# ３。MeCabに通す
  
# 学習する