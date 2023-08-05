import datetime
import json
import pymongo
# import dns.resolver
from pymongo import MongoClient
from pymongo import collection
from pymongo import ASCENDING,DESCENDING
from bson.json_util import dumps
from pymongo.common import CONNECT_TIMEOUT, RETRY_WRITES
from kisaan import subscription
import asyncio

# *************** calculate product price ***************
"""
calculate product price through unit,unit price and product weight
Note:specially design for double variation
"""
async def calculate_product_price(unit,unit_price,weight):
    unit=str(unit)
    unit_price=str(unit_price)
    weight=str(weight)

    if(len(unit.split(" "))==2):
        custom_unit_value,unit=unit.split(" ")
    else:
        custom_unit_value="1"

    weight_value,weight_unit=weight.split(" ")
    weight_unit_standard={"kg":1,"gm":1000,"liter":1,"ml":1000,"dozen":1,"piece":12}
    if(weight_unit_standard[unit]<weight_unit_standard[weight_unit]):
        price=eval(weight_value)*eval(unit_price)/(weight_unit_standard[unit]/eval(custom_unit_value))
        return price
    elif(weight_unit_standard[unit]==weight_unit_standard[weight_unit]):
        price=eval(weight_value)*eval(unit_price)/eval(custom_unit_value)
        return price
    elif(weight_unit_standard[unit]>weight_unit_standard[weight_unit]):
        return eval(weight_value)*eval(unit_price)*(weight_unit_standard[unit]/eval(custom_unit_value))

# *************** calculate delivery charges in total amount **************
"""
After pricing calculate delivery charges in recurring amount and one time amount
"""
async def calculate_delivery_charges(cluster_id,pricing_details,client):
    try:
        cluster=client["kisaan_webapp_prod"]["delivery_charge"]
        pipeline=[
            {"$match":{"cluster_id":cluster_id}}
            ]
        aggregation=cluster.aggregate(pipeline)
        delivery_charge=dumps(aggregation,indent=2).replace("\n","")
        delivery_charge=json.loads(delivery_charge)
        delivery_charge=delivery_charge[0]
        # print(delivery_charge)
        delivery_charge=delivery_charge["delivery_charges"]
    except:
        print("ERROR [Kisaan:Pricing:Calculate Delivery Charges]: Delivery charge not found in DB")
    try:
        for i in range(len(pricing_details["recurring_delivery_charges"])):
            print(pricing_details["recurring_delivery_charges"][i])
            for j in range(len(delivery_charge)):
                print(delivery_charge[j])
                recurring_amount=pricing_details["recurring_delivery_charges"][i]["recurring_amount"]
                if(delivery_charge[j]["condition"]=="exclusive-inclusive"):
                    if(recurring_amount>delivery_charge[j]["min_value"] and recurring_amount<=delivery_charge[j]["max_value"]):
                        pricing_details["recurring_delivery_charges"][i]["delivery_charge"]=delivery_charge[j]["delivery_charge"]
                elif(delivery_charge[j]["condition"]=="greater-than"):
                    if(recurring_amount>delivery_charge[j]["value"]):
                        pricing_details["recurring_delivery_charges"][i]["delivery_charge"]=0
    except:
        print("WARNING : no recurrinng order")

    total_amount=pricing_details["total_amount"]
    for k in range(len(delivery_charge)):
        if(delivery_charge[k]["condition"]=="exclusive-inclusive"):
            if(total_amount>delivery_charge[k]["min_value"] and total_amount<=delivery_charge[k]["max_value"]):
                pricing_details["today_delivery_charges"]=delivery_charge[k]["delivery_charge"]
        elif(delivery_charge[k]["condition"]=="greater-than"):
            if(total_amount>delivery_charge[k]["value"]):
                pricing_details["today_delivery_charges"]=delivery_charge[k]["delivery_charge"]
    discount=0
    # print(pricing_details)
    today_delivery_charges=pricing_details["today_delivery_charges"]
    total_payable_amount=total_amount+today_delivery_charges-discount
    pricing_details["discount"]=discount
    pricing_details["total_payable_amount"]=total_payable_amount

    return {"price_details":pricing_details,"delivery_charges":delivery_charge}   

# ******************** Calculate pricing of cart products ****************************

"""
Calculate the pricing of all the products of cart
"""

async def calculate_pricing_of_products(products):
    products=products
    total_amount=0
    one_time_amount=0

    pricing_details={"recurring_delivery_charges":[]}
    for i in range(len(products)):
        # print(products[i])
        if(products[i]["is_subscription"]==False):
            if(products[i]["type"]=="simple"):
                print("simple")
                item_count=products[i]["item_count"]
                price=products[i]["product_details"]["details"][0]["pricing_details"]["current_price"]
                current_amount=int(item_count)*price
                print("-------------------------------------------------------")
                print(current_amount)
                print(type(current_amount))
                    
                print(one_time_amount)
                print(type(one_time_amount))
                    
                one_time_amount=one_time_amount+current_amount
                total_amount=total_amount+current_amount
            elif(products[i]["type"]=="simple_variation"):
                print("simple variation")
                item_count=products[i]["item_count"]
                price=products[i]["product_details"]["details"][0]["pricing_details"]["current_price"]
                current_amount=item_count*price
                print(current_amount)
                one_time_amount=one_time_amount+current_amount
                total_amount=total_amount+current_amount
                # print(one_time_amount)
                # print(total_amount)
            elif(products[i]["type"]=="double_variation"):
                print("double variation")
                item_count=products[i]["item_count"]
                unit_price=products[i]["product_details"]["details"][0]["pricing_details"]["unit_price"]
                unit=products[i]["product_details"]["details"][0]["pricing_details"]["unit"]
                option=products[i]["product_details"]["details"][0]["attribute"]["option"]
                # print(cart.calculate_price(unit=unit,unit_price=unit_price,weight=option))
                current_amount=item_count*calculate_product_price(unit=unit,unit_price=unit_price,weight=option)
                print(current_amount)
                one_time_amount=one_time_amount+current_amount
                total_amount=total_amount+current_amount
                # print(one_time_amount)
                # print(total_amount)
        else:
            if(products[i]["type"]=="simple"):
                subscription_frequency=products[i]["subscription_frequency"]
                item_count=products[i]["item_count"]
                price=products[i]["product_details"]["details"][0]["pricing_details"]["current_price"]
                product_price=item_count*price
                total_amount=total_amount+product_price
                subscription_availability=await asyncio.gather(subscription.check_subscription_frequency(subscription_frequency,pricing_details["recurring_delivery_charges"]))
                subscription_availability=subscription_availability[0]
                # print(subscription_availability)
                if subscription_availability["status"]==False:
                    pricing_details["recurring_delivery_charges"].append(
                        {
                            "subscription_frequency":subscription_frequency,
                            "recurring_amount":product_price
                        }
                    )
                else:
                    pricing_details["recurring_delivery_charges"].remove(subscription_availability["subscription_data"])
                    subscription_availability["subscription_data"]["recurring_amount"]=subscription_availability["recurring_amount"]+product_price
                    pricing_details["recurring_delivery_charges"].append(subscription_availability["subscription_data"])
                    
            elif(products[i]["type"]=="simple_variation"):
                subscription_frequency=products[i]["subscription_frequency"]
                item_count=products[i]["item_count"]
                price=products[i]["product_details"]["details"][0]["pricing_details"]["current_price"]
                product_price=item_count*price
                total_amount=total_amount+product_price
                subscription_availability=subscription.check_subscription_frequency(subscription_frequency,pricing_details["recurring_delivery_charges"])
                if subscription_availability["status"]==False:
                    pricing_details["recurring_delivery_charges"].append(
                        {
                            "subscription_frequency":subscription_frequency,
                            "recurring_amount":product_price
                        }
                    )
                else:
                    pricing_details["recurring_delivery_charges"].remove(subscription_availability["subscription_data"])
                    subscription_availability["subscription_data"]["recurring_amount"]=subscription_availability["recurring_amount"]+product_price
                    pricing_details["recurring_delivery_charges"].append(subscription_availability["subscription_data"])
            elif(products[i]["type"]=="double_variation"):
                subscription_frequency=products[i]["subscription_frequency"]
                item_count=products[i]["item_count"]
                unit_price=products[i]["product_details"]["details"][0]["pricing_details"]["unit_price"]
                unit=products[i]["product_details"]["details"][0]["pricing_details"]["unit"]
                option=products[i]["product_details"]["details"][0]["attribute"]["option"]
                # print("-----------------------")
                print(calculate_product_price(unit=unit,unit_price=unit_price,weight=option))
                one_time_amount=one_time_amount+item_count*calculate_product_price(unit=unit,unit_price=unit_price,weight=option)
                total_amount=total_amount+product_price
                subscription_availability=subscription.check_subscription_frequency(subscription_frequency,pricing_details["recurring_delivery_charges"])
                if subscription_availability["status"]==False:
                    pricing_details["recurring_delivery_charges"].append(
                        {
                            "subscription_frequency":subscription_frequency,
                            "recurring_amount":product_price
                        }
                    )
                else:
                    pricing_details["recurring_delivery_charges"].remove(subscription_availability["subscription_data"])
                    subscription_availability["subscription_data"]["recurring_amount"]=subscription_availability["recurring_amount"]+product_price
                    pricing_details["recurring_delivery_charges"].append(subscription_availability["subscription_data"])
    # print(total_amount)
    # print(one_time_amount)
    pricing_details["total_amount"]=total_amount
    pricing_details["one_time_amount"]=one_time_amount
    if(len(pricing_details["recurring_delivery_charges"])==0):
        pricing_details.pop("recurring_delivery_charges")
    return pricing_details        



