import os

from init_setup import *


@app.route("/")
def home():
    os.system('cls')

    page_title = "Main Dashboard"
    front_data = {"title": [MAIN_TITLE, page_title, page_title],
                  "navbar": NAVBAR, }  # this dictionary is for frontend data (title, name, etc...)
    value_content = {
        "currency": CURRENCY,
    }  # this dictionary is mainly focus on content that have value (total, price, etc, ...)
    alert_data = {"title": "",
                  "msg": "",
                  "status": INFO_LEVEL[4]}

    # flash(json.dumps(alert_data))

    return render_template('index.html', front_data=front_data, value=value_content)


@app.route('/form/<form_type>', methods=['GET', 'POST'])
def form(form_type):
    os.system('cls')

    # setup variables
    timestamp_id = ts_id()
    page_title = "[Form] " + " ".join(form_type.split("-")).title()
    front_data = {"title": [MAIN_TITLE, page_title, "Form",
                            form_type],
                  "navbar": NAVBAR,
                  }  # this dictionary is for frontend data (title, name, etc...)
    value_content = {
        "currency": CURRENCY,
    }  # this dictionary is mainly focus on content that have value (total, price, etc, ...)
    alert_data = {"title": "",
                  "msg": "",
                  "status": INFO_LEVEL[5]}

    if form_type in FORM_TYPE:
        if form_type == FORM_TYPE[0]:
            item_data = {}

            # arrange shop data for the form
            try:
                for shop in dict(LOCAL_DATA['SHOPS']).keys():
                    if shop == "item_category" or shop == "item_unit":
                        value_content[shop] = sorted(LOCAL_DATA['SHOPS'][shop])
                        continue

                    item_data[shop] = {}

                    for item in dict(LOCAL_DATA['SHOPS'][shop]).keys():
                        if item != "index" and item not in item_data[shop]:
                            item_data[shop][item] = LOCAL_DATA['SHOPS'][shop][item]

                value_content['shops'] = item_data


            except Exception as e:
                create_logs("form-new-transaction", "app", f"Error: {e}", status='error')
                value_content['shops'] = {}

            value_content['cash_sources'] = list(dict(LOCAL_DATA['CASH_SOURCE']).keys())
            # print(value_content['shops'])

            shop_data = {
                'shop_name': "",
                'type': "",
                'cash_source': "",
                'tax': "",
                'date': "",
            }

            catch_itemData = {
                'item_name': "",
                'brand_name': "",
                'category': "",
                'quantity': "",
                'unit': "",
                'price': "",
                'total': "",
                'discount': "",
            }

            tags = [" ".join(tag.split("_")) for tag in catch_itemData.keys()]

            if request.method == "POST":
                # Process form data here
                shop_data['type'] = request.form['transaction_type']
                shop_data['shop_name'] = request.form['shop_name']
                shop_data['date'] = request.form['date']
                shop_data['cash_source'] = request.form['cash_source']
                shop_data['tax'] = request.form['tax']

                submit_transaction = [a for a in str(request.form['submit_transaction']).split(";") if a != ""]
                total_buy = 0

                # check if the year_month is already in the
                check_date = split_date(shop_data['date'], DATE_FT)
                check_month = f"{check_date[2]}_{check_date[1]}"

                # check transaction data
                if check_month not in LOCAL_DATA['TRANSACTION']:
                    LOCAL_DATA['TRANSACTION'][check_month] = {
                        f"{shop_data['cash_source']}": {f"{shop_data['date']}": {"IN": 0, "OUT": 0,
                                                                                 f"{shop_data['type']}": {
                                                                                     f"{shop_data['shop_name']}": {
                                                                                         "QTY": 0}}},
                                                        f"{shop_data['type']}": 0}}
                elif f"{shop_data['cash_source']}" not in LOCAL_DATA['TRANSACTION'][check_month]:
                    LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"] = {
                        f"{shop_data['date']}": {"IN": 0, "OUT": 0,
                                                 f"{shop_data['type']}": {f"{shop_data['shop_name']}": {"QTY": 0}}}}
                elif f"{shop_data['date']}" not in LOCAL_DATA['TRANSACTION'][check_month][
                    f"{shop_data['cash_source']}"]:
                    LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][f"{shop_data['date']}"] = {
                        "IN": 0, "OUT": 0, f"{shop_data['type']}": {f"{shop_data['shop_name']}": {"QTY": 0}}}
                elif f"{shop_data['type']}" not in \
                        LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][
                            f"{shop_data['date']}"]:
                    LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][f"{shop_data['date']}"][
                        f"{shop_data['type']}"] = {f"{shop_data['shop_name']}": {"QTY": 0}}
                elif f"{shop_data['shop_name']}" not in \
                        LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][f"{shop_data['date']}"][
                            f"{shop_data['type']}"]:
                    LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][f"{shop_data['date']}"][
                        f"{shop_data['type']}"] = {f"{shop_data['shop_name']}": {"QTY": 0}}

                if f"{shop_data['type']}" not in LOCAL_DATA['TRANSACTION'][check_month]:
                    LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['type']}"] = 0

                # check if shop exist or not
                if shop_data['shop_name'] not in LOCAL_DATA['SHOPS']:
                    LOCAL_DATA['SHOPS'][shop_data['shop_name']] = {
                        "index": 0,
                        "tax": shop_data['tax'],
                    }

                shop_info = LOCAL_DATA['SHOPS'][shop_data['shop_name']]
                transaction_save = LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][
                    f"{shop_data['date']}"]

                pprint(transaction_save, indent=2)

                if shop_info['tax'] != shop_data['tax']:
                    shop_info['tax'] = shop_data['tax']

                for tr in submit_transaction:
                    # save in catch_itemData
                    tr = tr.split(",")
                    print(tr, submit_transaction)
                    if len(tr) != len(catch_itemData.keys()):
                        if tr[0] == "OUTPAY":
                            if tr[0] not in transaction_save:
                                transaction_save[tr[0]] = []

                            if (tr[1], tr[2]) not in transaction_save[tr[0]]:
                                transaction_save[tr[0]].append((tr[1], numeric(tr[2])))
                            else:
                                for c, k in enumerate(list(transaction_save[tr[0]])):
                                    if k[0] == tr[1]:
                                        transaction_save[tr[0]][c] = (tr[1], numeric(tr[2]) + numeric(k[1]))
                                        break

                            total_buy += numeric(tr[2])
                        continue

                    for c, tag in enumerate(list(catch_itemData.keys())):
                        catch_itemData[tag] = numeric(str(tr[c]).rstrip())

                    # calculate total buy
                    if CURRENCY == "JPY":
                        total_buy += int(catch_itemData['total'])
                    else:
                        total_buy += float(catch_itemData['total'])

                    # check if brand exist inside shop or not
                    item_id = 0
                    if catch_itemData["brand_name"] not in shop_info:
                        shop_info[catch_itemData["brand_name"]] = {f"{catch_itemData['item_name']}": {
                            "category": catch_itemData['category'],
                            "1": [catch_itemData['unit'], catch_itemData['price']]
                        }}
                        shop_info["index"] += 1
                        item_id = 1
                    elif catch_itemData["item_name"] in shop_info[catch_itemData["brand_name"]]:
                        c = 0
                        for k in shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]]:
                            c += 1
                            if k == "category" and catch_itemData['category'] != \
                                    shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]]['category']:
                                shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]]['category'] = \
                                    catch_itemData['category']

                            elif [catch_itemData['unit'], numeric(catch_itemData['price'])] == \
                                    [shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][0],
                                     numeric(
                                         shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][1])]:
                                item_id = k
                                c = 0
                                break
                            elif catch_itemData['unit'] == \
                                    shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][0] and \
                                    catch_itemData['price'] != \
                                    shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][1]:
                                c = 0
                                item_id = k
                                shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][1] = numeric(
                                    catch_itemData[
                                        'price'])
                                break
                            elif catch_itemData['price'] == \
                                    shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][1] and \
                                    catch_itemData['unit'] != \
                                    shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][0]:
                                c = 0
                                item_id = k
                                shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][k][0] = \
                                    catch_itemData[
                                        'unit']
                                break

                        if c != 0:
                            shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][str(c)] = [
                                catch_itemData['unit'], numeric(catch_itemData['price'])]
                            item_id = c
                            shop_info["index"] += 1
                    elif catch_itemData["item_name"] not in shop_info[catch_itemData["brand_name"]]:
                        shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]] = {
                            "category": catch_itemData['category'],
                            "1": [catch_itemData['unit'], numeric(catch_itemData['price'])]
                        }
                        shop_info["index"] += 1
                        item_id = 1

                    # save category and unit in SHOPS
                    if "item_category" not in LOCAL_DATA['SHOPS']:
                        LOCAL_DATA['SHOPS']["item_category"] = [catch_itemData['category']]
                    elif catch_itemData['category'] not in LOCAL_DATA['SHOPS']["item_category"]:
                        LOCAL_DATA['SHOPS']["item_category"].append(catch_itemData['category'])

                    if "item_unit" not in LOCAL_DATA['SHOPS']:
                        LOCAL_DATA['SHOPS']["item_unit"] = [catch_itemData['unit']]
                    elif catch_itemData['unit'] not in LOCAL_DATA['SHOPS']["item_unit"]:
                        LOCAL_DATA['SHOPS']["item_unit"].append(catch_itemData['unit'])

                    # save in transaction
                    item_unit = shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][str(item_id)][0]
                    item_price = shop_info[catch_itemData["brand_name"]][catch_itemData["item_name"]][str(item_id)][1]
                    item_str = f"{catch_itemData['brand_name']}_{catch_itemData['item_name']}_{item_unit}_{item_price}"

                    if item_str not in transaction_save[f"{shop_data['type']}"][f"{shop_data['shop_name']}"]:
                        transaction_save[f"{shop_data['type']}"][f"{shop_data['shop_name']}"][item_str] = [1, numeric(
                            catch_itemData["discount"])]
                    else:
                        transaction_save[f"{shop_data['type']}"][f"{shop_data['shop_name']}"][item_str][0] += 1
                        transaction_save[f"{shop_data['type']}"][f"{shop_data['shop_name']}"][item_str][1] += numeric(
                            catch_itemData["discount"])

                    transaction_save[f"{shop_data['type']}"][f"{shop_data['shop_name']}"]["QTY"] += numeric(
                        catch_itemData['quantity'])

                # save in local data
                LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['cash_source']}"][
                    f"{shop_data['date']}"] = transaction_save
                LOCAL_DATA['SHOPS'][shop_data['shop_name']] = shop_info

                LOCAL_DATA['CASH_SOURCE'][shop_data['cash_source']]["AMOUNT"] -= total_buy
                transaction_save["OUT"] += total_buy
                LOCAL_DATA['TRANSACTION'][check_month][f"{shop_data['type']}"] += total_buy

                # update local check data
                LOCAL_DATA["_local"]["check"]["last_update"] = datetime_now()
                if "TRANSACTION" not in LOCAL_DATA["_local"]["check"]["updated_collections"]:
                    LOCAL_DATA["_local"]["check"]["updated_collections"].append("TRANSACTION")
                if "SHOPS" not in LOCAL_DATA["_local"]["check"]["updated_collections"]:
                    LOCAL_DATA["_local"]["check"]["updated_collections"].append("SHOPS")
                if "CASH_SOURCE" not in LOCAL_DATA["_local"]["check"]["updated_collections"]:
                    LOCAL_DATA["_local"]["check"]["updated_collections"].append("CASH_SOURCE")

                local_save_all(LOCAL_DATA)
                # save_test_local(LOCAL_DATA, "database/test_db.json")

                alert_data['title'] = "Transaction Submitted"
                alert_data['msg'] = f"Transaction submitted successfully. Date: {shop_data['date']}"
                alert_data['status'] = INFO_LEVEL[2]
                flash(json.dumps(alert_data))

                return redirect(url_for('form', form_type='new-transaction'))

            return render_template('form.html', data_tags=tags,
                                   front_data=front_data, value=value_content)

    else:
        abort(404)

    return render_template('form.html', front_data=front_data, content=value_content)


@app.route('/table/<table_type>')
def table(table_type):
    os.system('cls')

    page_title = "[Table] " + " ".join(table_type.split("-")).title()
    front_data = {"title": [MAIN_TITLE, page_title, "Tables",
                            table_type],
                  "navbar": NAVBAR,
                  }  # this dictionary is for frontend data (title, name, etc...)
    value_content = {
        "currency": CURRENCY,
    }  # this dictionary is mainly focus on content that have value (total, price, etc, ...)
    alert_data = {"title": "",
                  "msg": "",
                  "status": INFO_LEVEL[5]}

    if table_type in TRANSACTIONS_TYPE:
        if table_type == TRANSACTIONS_TYPE[0]:
            value_content['transactions'] = LOCAL_DATA['TRANSACTION']

            return render_template('table.html', front_data=front_data, content=value_content)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8000, debug=DEBUG)

    except KeyboardInterrupt:
        local_save_all(LOCAL_DATA)
        create_logs("app-exit", "app", "App stopped", status='info')

    except Exception as e:
        local_save_all(LOCAL_DATA)
        create_logs("app-error-catch", "app", f"Error: {e}", status='error')
