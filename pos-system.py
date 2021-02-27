import pandas as pd

# 商品クラス


class Item:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def get_price(self):
        return self.price

# オーダークラス


class Order:
    def __init__(self, item_master):
        self.item_order_list = []
        self.item_master = item_master

    def add_item_order(self, df_orderList):
        item_code = input('オーダーする商品のコードを入力してください。')
        Number_order = input('オーダーする商品の注文数を入力してください。')

        # item_codeを条件にitem_masterからindexを取得
        item_index = list(
            map(lambda x: x.item_code, self.item_master)).index(item_code)
        order_item = self.item_master[item_index]

        # オーダーされた商品がすでに登録済みかで分岐する
        if item_code in df_orderList.values:
            # オーダーされた商品がすでに登録済みの場合

            # オーダーリストから入力された商品コードに合致する情報を検索
            update_index = df_orderList[df_orderList['商品コード'].isin(
                [item_code])].index.values

            # すでに登録されている注文数に追加分を加算する
            num = str(
                int(df_orderList.iat[int(update_index), 3])
                + int(Number_order))

            # 個数、合計金額を更新
            df_orderList.iat[int(update_index), 3] = num
            df_orderList.iat[int(update_index), 4] = str(
                int(num) * int(df_orderList.iat[int(update_index), 2]))
        else:
            # オーダーされた商品が登録されていない場合

            # 入力された商品コードと個数をもとに、商品マスタの情報と合わせてオーダーリストに登録する
            df_orderList.loc[len(df_orderList)] = [
                item_code, order_item.item_name,
                order_item.price, Number_order,
                str(int(order_item.price) * int(Number_order))]
        self.item_order_list.append([item_code, Number_order])
        # 編集した情報でオーダーリストを更新
        df_orderList.to_csv('Order_list.csv')

    # オーダー表示関数
    def view_item_list(self, df_orderList):
        # 合計金額表示用変数
        sum_price = 0

        # オーダーリストから各商品の注文合計金額を抽出
        sum_price_list = df_orderList['合計金額'].tolist()

        # 合計金額を数値化
        for price in sum_price_list:
            sum_price += int(price)

        # 登録されているすべてのオーダー情報を出力する
        for item in self.item_order_list:
            # item_codeを条件にitem_masterからindexを取得
            item_index = list(
                map(lambda x: x.item_code, self.item_master)).index(item[0])
            # 取得したindexを使いitemを特定
            order_item = self.item_master[item_index]
            # 注文情報表示
            print("商品コード:{0}\t商品名：{1}\t価格：{2}\t注文数：{3}".format(
                item[0], order_item.item_name, order_item.price, item[1]))

        # 合計金額表示
        print('合計金額は{0}円です。'.format(sum_price))

        # pay_check = 0
        # なぜかwhileが実行されない
        # while pay_check > 0:
        pay = input('支払金額を入力してください。')
        if int(pay) > sum_price:
            print('おつりは{0}円です。'.format(int(pay)-sum_price))
            # pay_check = 1
        else:
            print('支払金額が足りません。')


# メイン処理
def main():
    # マスタ登録
    item_master = []

    df_item = pd.DataFrame(None, None, ['商品コード', '商品名', '価格'])
    # 数値で取り込まれると頭の0が消えるため、文字列でcsvを読み込む
    df_item = pd.read_csv('item_master.csv', dtype=str)
    # オーダーリスト用ファイルが存在していれば読み込む
    # 存在していなければデータファイルを新規作成
    try:
        df_orderList = pd.read_csv('Order_list.csv', dtype=str)
        df_orderList = df_orderList.drop(columns=df_orderList.columns[[0]])
    except FileNotFoundError:
        df_orderList = pd.DataFrame(
            None, None, ['商品コード', '商品名', '価格', '個数', '合計金額'])

    count = 0

    # csvの中身をマスタに登録する
    while len(df_item) > count:
        # 各行のデータを取得
        item_code = df_item.iloc[count, 1]
        item_name = df_item.iloc[count, 2]
        price = df_item.iloc[count, 3]
        # 取得したデータをマスタに登録
        item_master.append(Item(item_code, item_name, price))
        count += 1

    # オーダー登録
    order = Order(item_master)
    order.add_item_order(df_orderList)

    # オーダー表示
    order.view_item_list(df_orderList)


if __name__ == "__main__":
    main()
