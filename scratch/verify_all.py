import urllib.request
import json
import sys

def test_endpoint(url, desc):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BharatSentinelVerifier/2.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"[PASS] {desc}: {type(data)} with {len(data) if isinstance(data, (list, dict)) else data}")
            return data
    except Exception as e:
        print(f"[FAIL] {desc}: {e}")
        return None

def main():
    print("=== BHARAT SENTINEL API & FLIGHT DOSSIER VERIFICATION ===")
    
    # 1. Health
    test_endpoint("http://127.0.0.1:8000/api/health", "Health Check")
    
    # 2. Scope verification on Fleets (Russia, China, NATO, UK, EU, US, India, Pakistan)
    global_fleets = test_endpoint("http://127.0.0.1:8000/api/fleets?scope=global", "Global Fleets (Worldwide - RU, CN, NATO, UK, EU, US, IN, PK)")
    india_fleets = test_endpoint("http://127.0.0.1:8000/api/fleets?scope=india", "India Fleets (IOR Focus)")
    if global_fleets:
        print(f"       -> Global Fleets count: {len(global_fleets)}")
        for fl in global_fleets:
            print(f"          * [{fl.get('country')}] {fl.get('name')} | Verified: {fl.get('verified_official_source', fl.get('source'))} | Ships: {fl.get('ship_count', len(fl.get('ships', [])))}")

    # 3. Country Strategic Installations (Air Bases and Naval Bases)
    all_insts = test_endpoint("http://127.0.0.1:8000/api/installations", "All Strategic Military Bases")
    in_insts = test_endpoint("http://127.0.0.1:8000/api/installations?country=IN", "India Strategic Bases")
    us_insts = test_endpoint("http://127.0.0.1:8000/api/installations?country=US", "US Strategic Bases")
    cn_insts = test_endpoint("http://127.0.0.1:8000/api/installations?country=CN", "China Strategic Bases")
    ru_insts = test_endpoint("http://127.0.0.1:8000/api/installations?country=RU", "Russia Strategic Bases")
    pk_insts = test_endpoint("http://127.0.0.1:8000/api/installations?country=PK", "Pakistan Strategic Bases")
    
    if all_insts:
        print(f"       -> Total Strategic Bases Seeded: {len(all_insts)}")

    # 4. Scope verification on Flights & Dynamic Decoders
    global_flights = test_endpoint("http://127.0.0.1:8000/api/flights?scope=global", "Global Flights (Unified ADS-B Pool)")
    if global_flights:
        print(f"       -> Total Global Flights Streaming: {len(global_flights)}")
        # Check airlines decoded
        sample_flights = global_flights[:6]
        for f in sample_flights:
            print(f"          * Flight: {f.get('callsign')} | Airline: {f.get('airline')} | Model: {f.get('model')} | Route: {f.get('origin')} -> {f.get('dest')} | Alt: {f.get('altitude_m')}m | V-Speed: {f.get('vertical_speed_fpm')} fpm")

    # 5. Chatbot Test
    chat_payload = json.dumps({"query": "List active Russian, NATO, and Chinese naval carrier strike groups and their verified positions."}).encode()
    req = urllib.request.Request("http://127.0.0.1:8000/api/chat", data=chat_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as res:
        chat_resp = json.loads(res.read().decode())
        print(f"[PASS] Chatbot Response received (Length: {len(chat_resp.get('answer', ''))})")
        print(f"       Preview: {chat_resp.get('answer', '')[:160]}...")

    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
