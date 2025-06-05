#!/usr/bin/env python3
"""
Test script for Eid Al-Adha shipping offer functionality
Tests various scenarios to ensure the offer works correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8765"

def test_shipping_cost_calculation():
    """Test the shipping cost calculation with Eid offer"""
    print("🧪 Testing Eid Al-Adha Shipping Offer")
    print("=" * 50)
    
    # Test scenarios
    test_cases = [
        {
            "description": "Package #4 to Alexandria (Free shipping city)",
            "product_id": 4,
            "quantity": 1,
            "city_id": 1,  # Assuming Alexandria has city_id 1
            "expected_discount": "Free shipping"
        },
        {
            "description": "Package #4 to Cairo (Free shipping city)", 
            "product_id": 4,
            "quantity": 1,
            "city_id": 2,  # Assuming Cairo has city_id 2
            "expected_discount": "Free shipping"
        },
        {
            "description": "Package #4 to other governorate (50% discount)",
            "product_id": 4,
            "quantity": 1,
            "city_id": 10,  # Assuming this is not a free shipping city
            "expected_discount": "50% discount"
        },
        {
            "description": "Different package to Alexandria (No Eid offer)",
            "product_id": 1,  # Not package #4
            "quantity": 1,
            "city_id": 1,
            "expected_discount": "Regular pricing"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['description']}")
        print("-" * 40)
        
        # Test shipping cost calculation endpoint
        try:
            response = requests.post(
                f"{BASE_URL}/get_shipping_cost",
                data={
                    'product_id': test_case['product_id'],
                    'quantity': test_case['quantity'],
                    'city_id': test_case['city_id']
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
                
                # Check if Eid offer is applied
                if 'eid_offer' in result:
                    eid_info = result['eid_offer']
                    if eid_info.get('eligible'):
                        print(f"🎉 Eid Offer Applied: {eid_info.get('message', 'N/A')}")
                        print(f"💰 Discount: {eid_info.get('discount', 0) * 100}%")
                    else:
                        print("❌ Eid Offer Not Applied")
                else:
                    print("❌ No Eid Offer Information")
                    
            else:
                print(f"❌ Request failed with status: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing case: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing Complete")

def test_offer_timing():
    """Test if the offer is active during the correct time period"""
    print("\n⏰ Testing Offer Timing")
    print("-" * 30)
    
    offer_start = datetime(2025, 6, 5)
    offer_end = datetime(2025, 6, 11, 23, 59, 59)
    current_time = datetime.now()
    
    print(f"📅 Offer Start: {offer_start}")
    print(f"📅 Offer End: {offer_end}")
    print(f"📅 Current Time: {current_time}")
    
    if offer_start <= current_time <= offer_end:
        print("✅ Offer is currently ACTIVE")
    else:
        print("❌ Offer is currently INACTIVE")
        if current_time < offer_start:
            print(f"⏳ Offer starts in: {offer_start - current_time}")
        else:
            print(f"⏳ Offer ended: {current_time - offer_end} ago")

def check_database_cities():
    """Check what cities are in the database"""
    print("\n🏙️ Checking Database Cities")
    print("-" * 30)
    
    try:
        # We'll need to access the database to see city names and IDs
        # For now, let's test with known city IDs
        for city_id in range(1, 11):
            try:
                response = requests.post(
                    f"{BASE_URL}/get_shipping_cost",
                    data={
                        'product_id': 4,
                        'quantity': 1,
                        'city_id': city_id
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    print(f"City ID {city_id}: {result}")
            except:
                continue
                
    except Exception as e:
        print(f"❌ Error checking cities: {str(e)}")

if __name__ == "__main__":
    test_offer_timing()
    test_shipping_cost_calculation()
    check_database_cities()
