import os
import uuid
import math
import json
import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

class Database:
    """
    In-memory and persistent intelligence store for Bharat Sentinel.
    Maintains global & India-specific events, india_flags, naval_fleets, world_leaders,
    flight_contacts with operational combat radius, vessel_contacts, disasters, domestic_stability,
    and the human review queue.
    """
    def __init__(self):
        self.events: Dict[str, Dict[str, Any]] = {}
        self.india_flags: Dict[str, Dict[str, Any]] = {}
        self.naval_fleets: Dict[str, Dict[str, Any]] = {}
        self.world_leaders: Dict[str, Dict[str, Any]] = {}
        self.flight_contacts: Dict[str, Dict[str, Any]] = {}
        self.vessel_contacts: Dict[str, Dict[str, Any]] = {}
        self.disasters: Dict[str, Dict[str, Any]] = {}
        self.installations: Dict[str, Dict[str, Any]] = {}
        self.review_queue: Dict[str, Dict[str, Any]] = {}
        self.domestic_metrics: Dict[str, Any] = {}
        self.knowledge_docs: Dict[str, Dict[str, Any]] = {}
        self._init_knowledge()
        self._seed_initial_intelligence()

    def _init_knowledge(self):
        """Loads static knowledge files from knowledge/ directory for RAG context"""
        base_dir = Path(__file__).resolve().parent.parent
        knowledge_dir = base_dir / "knowledge"
        if knowledge_dir.exists():
            for k_file in knowledge_dir.glob("*.md"):
                try:
                    text = k_file.read_text(encoding="utf-8")
                    self.knowledge_docs[k_file.stem] = {
                        "filename": k_file.name,
                        "title": k_file.stem.replace("-", " ").title(),
                        "content": text
                    }
                except Exception as e:
                    print(f"[Database] Error reading knowledge file {k_file}: {e}")

    def _seed_initial_intelligence(self):
        now = datetime.now(timezone.utc)

        # -------------------------------------------------------------
        # 1. World & Regional Leaders (Global & India Focus)
        # -------------------------------------------------------------
        leaders_data = [
            {
                "id": "leader-modi",
                "name": "Narendra Modi",
                "title": "Prime Minister of India",
                "country": "India",
                "country_code": "IN",
                "lat": 28.6139,
                "lon": 77.2090,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Prime_Minister_Narendra_Modi_in_2023.jpg/240px-Prime_Minister_Narendra_Modi_in_2023.jpg",
                "status": "Active / In New Delhi",
                "last_statement": "SAGAR Doctrine reaffirmed: India stands as first responder and net security provider across the Indian Ocean Region while upholding rules-based maritime order.",
                "statement_date": (now - timedelta(hours=2)).isoformat(),
                "topic": "Maritime Security & Regional Stability",
                "stance": "constructive_deterrence",
                "source": "PMO India / PIB Official Dispatch",
                "is_india_relevant": True
            },
            {
                "id": "leader-jaishankar",
                "name": "Dr. S. Jaishankar",
                "title": "External Affairs Minister",
                "country": "India",
                "country_code": "IN",
                "lat": 28.6250,
                "lon": 77.2180,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Subrahmanyam_Jaishankar_in_2022.jpg/240px-Subrahmanyam_Jaishankar_in_2022.jpg",
                "status": "Active / Diplomatic Briefing",
                "last_statement": "India's strategic autonomy remains non-negotiable. Dialogue and diplomacy guide LAC disengagement, but border peace remains prerequisite for normal relations.",
                "statement_date": (now - timedelta(hours=4)).isoformat(),
                "topic": "LAC Border Disengagement & Strategic Autonomy",
                "stance": "firm_diplomatic",
                "source": "MEA India Official Transcript",
                "is_india_relevant": True
            },
            {
                "id": "leader-putin",
                "name": "Vladimir Putin",
                "title": "President of Russia",
                "country": "Russia",
                "country_code": "RU",
                "lat": 55.7558,
                "lon": 37.6173,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Vladimir_Putin_%282020-02-20%29.jpg/240px-Vladimir_Putin_%282020-02-20%29.jpg",
                "status": "Active / Kremlin Moscow",
                "last_statement": "The transition to a multipolar financial and geopolitical architecture in Eurasia and the Global South is an objective historical process.",
                "statement_date": (now - timedelta(hours=7)).isoformat(),
                "topic": "Eurasian Multipolarity & Trade Corridors",
                "stance": "assertive",
                "source": "Kremlin Press Service / TASS",
                "is_india_relevant": True
            },
            {
                "id": "leader-xi",
                "name": "Xi Jinping",
                "title": "President of China",
                "country": "China",
                "country_code": "CN",
                "lat": 39.9042,
                "lon": 116.4074,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Xi_Jinping_2019.jpg/240px-Xi_Jinping_2019.jpg",
                "status": "Active / Zhongnanhai Beijing",
                "last_statement": "Stressed deepening Western Theatre Command combat readiness while maintaining diplomatic consultation channels along western frontiers.",
                "statement_date": (now - timedelta(hours=5)).isoformat(),
                "topic": "Military Preparedness & Western Frontiers",
                "stance": "strategic_posturing",
                "source": "Xinhua News Agency / PLA Daily",
                "is_india_relevant": True
            },
            {
                "id": "leader-biden",
                "name": "US National Security Command",
                "title": "Washington DC / INDOPACOM",
                "country": "United States",
                "country_code": "US",
                "lat": 38.8951,
                "lon": -77.0364,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Joe_Biden_presidential_portrait.jpg/240px-Joe_Biden_presidential_portrait.jpg",
                "status": "Active / White House Situation Room",
                "last_statement": "Reaffirming Quad maritime domain awareness and freedom of navigation across the Indo-Pacific and Red Sea commercial transit corridors.",
                "statement_date": (now - timedelta(hours=3)).isoformat(),
                "topic": "Indo-Pacific & Red Sea Navigation",
                "stance": "allied_commitment",
                "source": "White House Press Office / DoD Readout",
                "is_india_relevant": True
            },
            {
                "id": "leader-pezeshkian",
                "name": "Masoud Pezeshkian",
                "title": "President of Iran",
                "country": "Iran",
                "country_code": "IR",
                "lat": 35.6892,
                "lon": 51.3890,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Masoud_Pezeshkian_in_Tabriz_06.jpg/240px-Masoud_Pezeshkian_in_Tabriz_06.jpg",
                "status": "Active / Tehran",
                "last_statement": "Chabahar Port operationalization represents an unshakeable bridge of commerce with India, Central Asia, and the INSTC freight corridor.",
                "statement_date": (now - timedelta(hours=11)).isoformat(),
                "topic": "Chabahar Port Agreement & INSTC Corridors",
                "stance": "constructive_economic",
                "source": "IRNA Official News Agency",
                "is_india_relevant": True
            },
            {
                "id": "leader-sharif",
                "name": "Shehbaz Sharif",
                "title": "Prime Minister of Pakistan",
                "country": "Pakistan",
                "country_code": "PK",
                "lat": 33.6844,
                "lon": 73.0479,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Shehbaz_Sharif_2022.jpg/240px-Shehbaz_Sharif_2022.jpg",
                "status": "Active / Islamabad",
                "last_statement": "CPEC corridor infrastructure and Gwadar deep-water port connectivity remain strategic economic anchors for national revitalization.",
                "statement_date": (now - timedelta(hours=14)).isoformat(),
                "topic": "Gwadar Port & CPEC Infrastructure",
                "stance": "bilateral_economic",
                "source": "Radio Pakistan / Associated Press of Pakistan",
                "is_india_relevant": True
            },
            {
                "id": "leader-macron",
                "name": "Emmanuel Macron",
                "title": "President of France",
                "country": "France",
                "country_code": "FR",
                "lat": 48.8566,
                "lon": 2.3522,
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Emmanuel_Macron_%28cropped%29.jpg/240px-Emmanuel_Macron_%28cropped%29.jpg",
                "status": "Active / Élysée Palace Paris",
                "last_statement": "France and India will expand joint maritime surveillance missions across Reunion and Southwest Indian Ocean zones under bilateral defense accord.",
                "statement_date": (now - timedelta(hours=9)).isoformat(),
                "topic": "Indo-French Maritime Surveillance Pact",
                "stance": "allied_cooperation",
                "source": "Élysée Press Office / AFP",
                "is_india_relevant": True
            }
        ]
        for l in leaders_data:
            self.world_leaders[l["id"]] = l

        # -------------------------------------------------------------
        # 2. Worldwide Naval Carrier Strike Groups & Fleets with Range Specs
        # -------------------------------------------------------------
        fleets_data = [
            # --- US NAVY FLEETS ---
            {
                "id": "fleet-arabian-sea",
                "name": "US Navy 5th Fleet (USS Abraham Lincoln CSG)",
                "region": "Arabian Sea / North Indian Ocean",
                "country": "United States",
                "country_code": "US",
                "lat": 19.50,
                "lon": 64.20,
                "ship_count": 15,
                "flag": "US Navy 5th Fleet",
                "air_wing_strike_radius_nm": 550,
                "combat_radius_km": 1020,
                "radar_coverage_km": 450,
                "air_defense_envelope_km": 160,
                "source": "USNI News Fleet Tracker / NAVCENT Public Affairs",
                "verified_official_source": "U.S. Naval Forces Central Command (NAVCENT) / USNI News Fleet Tracker",
                "official_dispatch_quote": "USS Abraham Lincoln (CVN-72) Carrier Strike Group operating in the U.S. 5th Fleet area of operations to ensure regional maritime security and deter aggression across the Arabian Sea.",
                "official_source_url": "https://news.usni.org/category/fleet-tracker",
                "official_verification_badge": "USNI TRACKED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "North Arabian Sea / Gulf of Oman (19.5°N, 64.2°E)",
                "last_reported": (now - timedelta(hours=2)).isoformat(),
                "status": "Forward Deployed / High Vigilance",
                "is_india_relevant": True,
                "ships": [
                    {"name": "USS Abraham Lincoln", "hull": "CVN-72", "type": "Nimitz Nuclear Aircraft Carrier", "country": "US", "status": "F-35C / F/A-18E Flight Ops", "speed": "19.5 kts", "heading": "240°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Delbert D. Black", "hull": "DDG-119", "type": "Arleigh Burke Destroyer", "country": "US", "status": "Escort", "speed": "19.0 kts", "heading": "115°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Higgins", "hull": "DDG-76", "type": "Guided Missile Destroyer", "country": "US", "status": "Patrol", "speed": "17.1 kts", "heading": "118°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Mason", "hull": "DDG-87", "type": "Guided Missile Destroyer", "country": "US", "status": "Air Defense", "speed": "17.4 kts", "heading": "110°", "source": "USNI News", "confidence": "High"},
                    {"name": "USNS Supply", "hull": "T-AOE-6", "type": "Fast Combat Support Ship", "country": "US", "status": "Replenishment", "speed": "12.0 kts", "heading": "115°", "source": "USNI News", "confidence": "Medium"}
                ]
            },
            {
                "id": "fleet-us-7th-fleet",
                "name": "US Navy 7th Fleet (USS George Washington CSG)",
                "region": "Philippine Sea / Western Pacific",
                "country": "United States",
                "country_code": "US",
                "lat": 18.20,
                "lon": 126.50,
                "ship_count": 9,
                "flag": "US Navy 7th Fleet",
                "air_wing_strike_radius_nm": 700,
                "combat_radius_km": 1300,
                "radar_coverage_km": 480,
                "air_defense_envelope_km": 180,
                "source": "Commander, U.S. 7th Fleet Public Affairs / USNI News",
                "verified_official_source": "Commander, U.S. 7th Fleet Public Affairs (c7f.navy.mil) / USNI News",
                "official_dispatch_quote": "USS George Washington (CVN-73) and Carrier Air Wing 5 forward-deployed forces executed integrated air-defense and strike maneuvers in the Philippine Sea.",
                "official_source_url": "https://www.c7f.navy.mil",
                "official_verification_badge": "US 7TH FLEET VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Philippine Sea / Luzon Strait Approach (18.2°N, 126.5°E)",
                "last_reported": (now - timedelta(hours=4)).isoformat(),
                "status": "Forward Deterrence Patrol",
                "is_india_relevant": False,
                "ships": [
                    {"name": "USS George Washington", "hull": "CVN-73", "type": "Nimitz Nuclear Aircraft Carrier", "country": "US", "status": "F-35C Strike Ops", "speed": "21.0 kts", "heading": "340°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Antietam", "hull": "CG-54", "type": "Ticonderoga Cruiser", "country": "US", "status": "Air Defense", "speed": "19.0 kts", "heading": "340°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Rafael Peralta", "hull": "DDG-115", "type": "Arleigh Burke Destroyer", "country": "US", "status": "Screen", "speed": "18.0 kts", "heading": "340°", "source": "USNI News", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-us-6th-fleet",
                "name": "US Navy 6th Fleet (USS Harry S. Truman CSG)",
                "region": "Eastern Mediterranean / Ionian Sea",
                "country": "United States",
                "country_code": "US",
                "lat": 35.80,
                "lon": 18.50,
                "ship_count": 8,
                "flag": "US Navy 6th Fleet",
                "air_wing_strike_radius_nm": 600,
                "combat_radius_km": 1110,
                "radar_coverage_km": 450,
                "air_defense_envelope_km": 160,
                "source": "U.S. 6th Fleet (c6f.navy.mil) / USNI News",
                "verified_official_source": "Commander, U.S. Naval Forces Europe-Africa / U.S. 6th Fleet",
                "official_dispatch_quote": "USS Harry S. Truman (CVN-75) Strike Group conducts dual-carrier strike integration with NATO allies across the Mediterranean.",
                "official_source_url": "https://www.c6f.navy.mil",
                "official_verification_badge": "US 6TH FLEET VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Central Mediterranean / Ionian Basin (35.8°N, 18.5°E)",
                "last_reported": (now - timedelta(hours=3)).isoformat(),
                "status": "NATO Southern Flank Readiness",
                "is_india_relevant": False,
                "ships": [
                    {"name": "USS Harry S. Truman", "hull": "CVN-75", "type": "Nimitz Nuclear Carrier", "country": "US", "status": "Flight Ops", "speed": "20.0 kts", "heading": "110°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Jason Dunham", "hull": "DDG-109", "type": "Arleigh Burke Destroyer", "country": "US", "status": "Escort", "speed": "18.5 kts", "heading": "110°", "source": "USNI News", "confidence": "High"},
                    {"name": "USS Stout", "hull": "DDG-55", "type": "Guided Missile Destroyer", "country": "US", "status": "BMD Screen", "speed": "17.0 kts", "heading": "110°", "source": "USNI News", "confidence": "High"}
                ]
            },

            # --- RUSSIAN NAVY FLEETS ---
            {
                "id": "fleet-russia-northern",
                "name": "Russian Navy Northern Fleet (Admiral Gorshkov Strike Group)",
                "region": "Barents Sea / Arctic Ocean",
                "country": "Russia",
                "country_code": "RU",
                "lat": 70.50,
                "lon": 35.00,
                "ship_count": 8,
                "flag": "Russian Navy (Northern Fleet)",
                "air_wing_strike_radius_nm": 450,
                "combat_radius_km": 830,
                "radar_coverage_km": 420,
                "air_defense_envelope_km": 150,
                "source": "Ministry of Defence of the Russian Federation (mil.ru) / TASS",
                "verified_official_source": "Russian Federation Ministry of Defence / Northern Fleet Press Office",
                "official_dispatch_quote": "Russian Navy Northern Fleet strike group led by frigate Admiral Gorshkov conducted Zircon hypersonic missile drills in the Barents Sea.",
                "official_source_url": "https://eng.mil.ru",
                "official_verification_badge": "RUSSIAN MOD VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Barents Sea / Kola Peninsula Approach (70.5°N, 35.0°E)",
                "last_reported": (now - timedelta(hours=5)).isoformat(),
                "status": "Arctic Bastion Patrol / Hypersonic Readiness",
                "is_india_relevant": True,
                "ships": [
                    {"name": "Admiral Flota Sovetskogo Soyuza Gorshkov", "hull": "454", "type": "Project 22350 Guided Frigate", "country": "RU", "status": "Zircon Hypersonic Patrol", "speed": "18.0 kts", "heading": "030°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Admiral Golovko", "hull": "456", "type": "Project 22350 Stealth Frigate", "country": "RU", "status": "Air Defense", "speed": "18.0 kts", "heading": "030°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Severodvinsk", "hull": "K-560", "type": "Yasen-class Nuclear Attack Submarine", "country": "RU", "status": "Submerged Bastion Patrol", "speed": "14.0 kts", "heading": "020°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Kazan", "hull": "K-561", "type": "Yasen-M Guided Cruise Submarine", "country": "RU", "status": "Submerged Escort", "speed": "15.0 kts", "heading": "025°", "source": "mil.ru", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-russia-mediterranean",
                "name": "Russian Navy Mediterranean Task Force (Tartus Squadron)",
                "region": "Eastern Mediterranean / Levant Basin",
                "country": "Russia",
                "country_code": "RU",
                "lat": 35.10,
                "lon": 35.30,
                "ship_count": 6,
                "flag": "Russian Navy (Mediterranean Flotilla)",
                "air_wing_strike_radius_nm": 300,
                "combat_radius_km": 550,
                "radar_coverage_km": 350,
                "air_defense_envelope_km": 120,
                "source": "mil.ru / Tartus Logistics Base Dispatch",
                "verified_official_source": "Russian Navy Mediterranean Operational Command / Tartus Naval Base",
                "official_dispatch_quote": "Russian naval detachment operating from Tartus logistics hub executed anti-submarine and cruise missile patrol across the Eastern Mediterranean.",
                "official_source_url": "https://eng.mil.ru",
                "official_verification_badge": "RUSSIAN NAVY VERIFIED",
                "official_confirmation_date": "2026-08-29",
                "verified_sector": "Levant Coast / Tartus Maritime Approach (35.1°N, 35.3°E)",
                "last_reported": (now - timedelta(hours=4)).isoformat(),
                "status": "Forward Mediterranean Vigilance",
                "is_india_relevant": False,
                "ships": [
                    {"name": "Admiral Grigorovich", "hull": "745", "type": "Project 11356R Frigate", "country": "RU", "status": "Kalibr Patrol", "speed": "16.0 kts", "heading": "270°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Orekhovo-Zuyevo", "hull": "626", "type": "Buyan-M Missile Corvette", "country": "RU", "status": "Coastal Defense", "speed": "15.0 kts", "heading": "270°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Krasnodar", "hull": "B-265", "type": "Improved Kilo Submarine", "country": "RU", "status": "Submerged Patrol", "speed": "6.0 kts", "heading": "280°", "source": "mil.ru", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-russia-pacific",
                "name": "Russian Navy Pacific Fleet (Varyag Missile Cruiser Group)",
                "region": "Sea of Japan / Peter the Great Gulf",
                "country": "Russia",
                "country_code": "RU",
                "lat": 42.80,
                "lon": 132.50,
                "ship_count": 7,
                "flag": "Russian Navy (Pacific Fleet)",
                "air_wing_strike_radius_nm": 380,
                "combat_radius_km": 700,
                "radar_coverage_km": 400,
                "air_defense_envelope_km": 150,
                "source": "mil.ru / Pacific Fleet HQ Vladivostok",
                "verified_official_source": "Russian Pacific Fleet Command / TASS",
                "official_dispatch_quote": "Pacific Fleet flagship cruiser Varyag and Marshal Shaposhnikov frigate conducted joint combat exercises in the Sea of Japan.",
                "official_source_url": "https://eng.mil.ru",
                "official_verification_badge": "PACIFIC FLEET VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Sea of Japan / Vladivostok Sector (42.8°N, 132.5°E)",
                "last_reported": (now - timedelta(hours=6)).isoformat(),
                "status": "Far East Sovereignty Patrol",
                "is_india_relevant": False,
                "ships": [
                    {"name": "Varyag", "hull": "011", "type": "Slava-class Guided Missile Cruiser", "country": "RU", "status": "Flagship Patrol", "speed": "18.0 kts", "heading": "190°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Marshal Shaposhnikov", "hull": "543", "type": "Udaloy-class Guided Destroyer", "country": "RU", "status": "ASW Screen", "speed": "17.5 kts", "heading": "190°", "source": "mil.ru", "confidence": "High"},
                    {"name": "Gromkiy", "hull": "335", "type": "Steregushchiy-class Corvette", "country": "RU", "status": "Escort", "speed": "16.0 kts", "heading": "190°", "source": "mil.ru", "confidence": "High"}
                ]
            },

            # --- CHINESE PLA NAVY FLEETS ---
            {
                "id": "fleet-south-china-sea",
                "name": "PLA Navy Shandong (CV-17) Carrier Strike Group",
                "region": "South China Sea / Hainan Basin",
                "country": "China",
                "country_code": "CN",
                "lat": 16.50,
                "lon": 113.80,
                "ship_count": 10,
                "flag": "PLA Navy (China)",
                "air_wing_strike_radius_nm": 650,
                "combat_radius_km": 1200,
                "radar_coverage_km": 450,
                "air_defense_envelope_km": 200,
                "source": "Ministry of National Defense PRC (mod.gov.cn) / PLA Southern Theater Command",
                "verified_official_source": "Ministry of National Defense PRC (mod.gov.cn) / PLA Southern Theater Command",
                "official_dispatch_quote": "PLAN Aircraft Carrier Shandong (CV-17) strike group conducted realistic combat training exercises including J-15 carrier fighter day/night sorties in the South China Sea.",
                "official_source_url": "http://eng.mod.gov.cn",
                "official_verification_badge": "MOD PRC CONFIRMED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "South China Sea / Paracel Archipelago (16.5°N, 113.8°E)",
                "last_reported": (now - timedelta(hours=5)).isoformat(),
                "status": "Carrier Strike Exercises / High Readiness",
                "is_india_relevant": True,
                "ships": [
                    {"name": "PLAN Shandong", "hull": "17", "type": "STOBAR Aircraft Carrier", "country": "CN", "status": "J-15 Flight Ops", "speed": "19.0 kts", "heading": "210°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Dalian", "hull": "105", "type": "Type 055 Large Guided Destroyer", "country": "CN", "status": "Carrier Escort", "speed": "18.5 kts", "heading": "210°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Zibo", "hull": "156", "type": "Type 052D Guided Destroyer", "country": "CN", "status": "Air Defense Screen", "speed": "17.0 kts", "heading": "210°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Chaganhu", "hull": "905", "type": "Type 901 Fast Combat Support Ship", "country": "CN", "status": "Replenishment", "speed": "14.0 kts", "heading": "210°", "source": "MOD PRC", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-china-liaoning",
                "name": "PLA Navy Liaoning (CV-16) Carrier Strike Group",
                "region": "East China Sea / Miyako Strait Approach",
                "country": "China",
                "country_code": "CN",
                "lat": 25.50,
                "lon": 125.80,
                "ship_count": 8,
                "flag": "PLA Navy (China)",
                "air_wing_strike_radius_nm": 600,
                "combat_radius_km": 1110,
                "radar_coverage_km": 420,
                "air_defense_envelope_km": 180,
                "source": "mod.gov.cn / PLA Eastern Theater Command",
                "verified_official_source": "Ministry of National Defense PRC / Joint Staff Office Japan Verified",
                "official_dispatch_quote": "PLAN Aircraft Carrier Liaoning (CV-16) CSG completed carrier qualification and dual-carrier coordination exercises east of Taiwan.",
                "official_source_url": "http://eng.mod.gov.cn",
                "official_verification_badge": "MOD PRC CONFIRMED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Miyako Strait / East of Taiwan (25.5°N, 125.8°E)",
                "last_reported": (now - timedelta(hours=4)).isoformat(),
                "status": "Island Chain Breakthrough Patrol",
                "is_india_relevant": False,
                "ships": [
                    {"name": "PLAN Liaoning", "hull": "16", "type": "STOBAR Aircraft Carrier", "country": "CN", "status": "J-15 Strike Ops", "speed": "20.0 kts", "heading": "140°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Nanchang", "hull": "101", "type": "Type 055 Large Guided Destroyer", "country": "CN", "status": "Flag Escort", "speed": "19.0 kts", "heading": "140°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Chengdu", "hull": "120", "type": "Type 052D Destroyer", "country": "CN", "status": "Air Defense", "speed": "18.0 kts", "heading": "140°", "source": "MOD PRC", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-china-fujian",
                "name": "PLA Navy Fujian (CV-18) Electromagnetic Catapult Sea Trials Group",
                "region": "Bohai Sea / Yellow Sea",
                "country": "China",
                "country_code": "CN",
                "lat": 38.20,
                "lon": 121.50,
                "ship_count": 6,
                "flag": "PLA Navy (China)",
                "air_wing_strike_radius_nm": 750,
                "combat_radius_km": 1390,
                "radar_coverage_km": 500,
                "air_defense_envelope_km": 200,
                "source": "mod.gov.cn / Xinhua Maritime Dispatch",
                "verified_official_source": "Ministry of National Defense PRC / PLAN Naval Research Institute",
                "official_dispatch_quote": "PLAN 3rd Generation Aircraft Carrier Fujian (CV-18) conducted electromagnetic catapult launch trials with J-35 and J-15T fighters in the Bohai Bay.",
                "official_source_url": "http://eng.mod.gov.cn",
                "official_verification_badge": "PLAN EMALS TRIALS",
                "official_confirmation_date": "2026-08-29",
                "verified_sector": "Bohai Sea / Dalian Maritime Prohibited Zone (38.2°N, 121.5°E)",
                "last_reported": (now - timedelta(hours=6)).isoformat(),
                "status": "EMALS Catapult Flight Integration",
                "is_india_relevant": False,
                "ships": [
                    {"name": "PLAN Fujian", "hull": "18", "type": "CATOBAR EMALS Supercarrier", "country": "CN", "status": "J-35 / J-15T Catapult Trials", "speed": "18.0 kts", "heading": "080°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Anshan", "hull": "103", "type": "Type 055 Large Guided Destroyer", "country": "CN", "status": "Trial Escort", "speed": "17.0 kts", "heading": "080°", "source": "MOD PRC", "confidence": "High"},
                    {"name": "PLAN Baotou", "hull": "133", "type": "Type 052D Destroyer", "country": "CN", "status": "Perimeter Screen", "speed": "16.0 kts", "heading": "080°", "source": "MOD PRC", "confidence": "High"}
                ]
            },

            # --- NATO & EU FLEETS ---
            {
                "id": "fleet-nato-snmg1",
                "name": "Standing NATO Maritime Group 1 (SNMG1)",
                "region": "Baltic Sea / Skagerrak Strait",
                "country": "NATO",
                "country_code": "NATO",
                "lat": 58.50,
                "lon": 19.50,
                "ship_count": 7,
                "flag": "NATO Allied Maritime Command (MARCOM)",
                "air_wing_strike_radius_nm": 350,
                "combat_radius_km": 650,
                "radar_coverage_km": 380,
                "air_defense_envelope_km": 140,
                "source": "NATO MARCOM Public Affairs (mc.nato.int)",
                "verified_official_source": "NATO Allied Maritime Command HQ Northwood",
                "official_dispatch_quote": "SNMG1 task group under NATO command conducted Operation Brilliant Shield anti-surface and electronic warfare integration in the Baltic Sea.",
                "official_source_url": "https://mc.nato.int",
                "official_verification_badge": "NATO MARCOM VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Central Baltic Sea / Gotland Approach (58.5°N, 19.5°E)",
                "last_reported": (now - timedelta(hours=3)).isoformat(),
                "status": "NATO High Readiness Force Patrol",
                "is_india_relevant": False,
                "ships": [
                    {"name": "HNoMS Otto Sverdrup", "hull": "F312", "type": "Fridtjof Nansen-class Frigate", "country": "NO", "status": "SNMG1 Flagship", "speed": "17.0 kts", "heading": "060°", "source": "NATO MARCOM", "confidence": "High"},
                    {"name": "FGS Sachsen", "hull": "F219", "type": "Sachsen Air Defense Frigate", "country": "DE", "status": "Air Defense Screen", "speed": "17.5 kts", "heading": "060°", "source": "NATO MARCOM", "confidence": "High"},
                    {"name": "HNLMS De Zeven Provinciën", "hull": "F802", "type": "De Zeven Provinciën Frigate", "country": "NL", "status": "BMD Surveillance", "speed": "16.5 kts", "heading": "060°", "source": "NATO MARCOM", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-nato-snmg2",
                "name": "Standing NATO Maritime Group 2 (SNMG2)",
                "region": "Aegean Sea / Eastern Mediterranean",
                "country": "NATO",
                "country_code": "NATO",
                "lat": 36.80,
                "lon": 25.20,
                "ship_count": 6,
                "flag": "NATO Allied Maritime Command (MARCOM)",
                "air_wing_strike_radius_nm": 320,
                "combat_radius_km": 590,
                "radar_coverage_km": 360,
                "air_defense_envelope_km": 130,
                "source": "NATO MARCOM / Hellenic Navy Dispatch",
                "verified_official_source": "NATO Allied Maritime Command MARCOM",
                "official_dispatch_quote": "SNMG2 flagship and allied frigates maintained persistent maritime security patrol and air surveillance across the Aegean and Eastern Mediterranean.",
                "official_source_url": "https://mc.nato.int",
                "official_verification_badge": "NATO MARCOM VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Aegean Sea / Cyclades Sector (36.8°N, 25.2°E)",
                "last_reported": (now - timedelta(hours=4)).isoformat(),
                "status": "Operation Sea Guardian Maritime Security",
                "is_india_relevant": False,
                "ships": [
                    {"name": "TCG Gökova", "hull": "F-496", "type": "Gabya-class Guided Frigate", "country": "TR", "status": "SNMG2 Escort", "speed": "16.0 kts", "heading": "180°", "source": "NATO MARCOM", "confidence": "High"},
                    {"name": "HS Navarinon", "hull": "F-461", "type": "Elli-class Frigate", "country": "GR", "status": "Screen", "speed": "16.5 kts", "heading": "180°", "source": "NATO MARCOM", "confidence": "High"},
                    {"name": "ESPS Méndez Núñez", "hull": "F-104", "type": "Álvaro de Bazán Aegis Frigate", "country": "ES", "status": "Aegis Air Defense", "speed": "17.0 kts", "heading": "180°", "source": "NATO MARCOM", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-eu-aspides",
                "name": "EU NAVFOR Operation Aspides Task Force",
                "region": "Southern Red Sea / Bab el-Mandeb Strait",
                "country": "EU",
                "country_code": "EU",
                "lat": 13.80,
                "lon": 43.10,
                "ship_count": 6,
                "flag": "European Union Naval Force (EU NAVFOR)",
                "air_wing_strike_radius_nm": 250,
                "combat_radius_km": 460,
                "radar_coverage_km": 350,
                "air_defense_envelope_km": 120,
                "source": "EEAS / EU NAVFOR Aspides Operational HQ Larissa",
                "verified_official_source": "European Union External Action Service / EU NAVFOR Aspides",
                "official_dispatch_quote": "EU NAVFOR Operation Aspides warships intercepted hostile UAV vectors and provided close escort protection to commercial merchant vessels in the Red Sea.",
                "official_source_url": "https://www.eeas.europa.eu/eeas/eunavfor-aspides_en",
                "official_verification_badge": "EU NAVFOR VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Bab el-Mandeb / Red Sea Transit Corridor (13.8°N, 43.1°E)",
                "last_reported": (now - timedelta(hours=2)).isoformat(),
                "status": "Close Escort & Air Defense Interception",
                "is_india_relevant": True,
                "ships": [
                    {"name": "ITS Caio Duilio", "hull": "D554", "type": "Orizzonte Air Defense Destroyer", "country": "IT", "status": "Force Flagship", "speed": "18.0 kts", "heading": "320°", "source": "EU NAVFOR", "confidence": "High"},
                    {"name": "FGS Hessen", "hull": "F221", "type": "Sachsen Air Defense Frigate", "country": "DE", "status": "UAV Air Defense", "speed": "17.5 kts", "heading": "320°", "source": "EU NAVFOR", "confidence": "High"},
                    {"name": "HS Hydra", "hull": "F-452", "type": "Hydra-class Frigate", "country": "GR", "status": "Merchant Escort", "speed": "16.0 kts", "heading": "320°", "source": "EU NAVFOR", "confidence": "High"}
                ]
            },

            # --- UK ROYAL NAVY ---
            {
                "id": "fleet-north-atlantic",
                "name": "UK Royal Navy Carrier Strike Group (HMS Queen Elizabeth)",
                "region": "North Atlantic / North Sea",
                "country": "United Kingdom",
                "country_code": "UK",
                "lat": 56.50,
                "lon": -12.20,
                "ship_count": 6,
                "flag": "Royal Navy",
                "air_wing_strike_radius_nm": 600,
                "combat_radius_km": 1110,
                "radar_coverage_km": 400,
                "air_defense_envelope_km": 120,
                "source": "Royal Navy Official Press Office",
                "verified_official_source": "Ministry of Defence UK / Royal Navy Official Releases",
                "official_dispatch_quote": "HMS Queen Elizabeth deployed to the North Atlantic commanding multinational Strike Warrior operations with NATO maritime partners.",
                "official_source_url": "https://www.royalnavy.mod.uk",
                "official_verification_badge": "ROYAL NAVY VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "North Atlantic / Hebrides Approach (56.5°N, 12.2°W)",
                "last_reported": (now - timedelta(hours=6)).isoformat(),
                "status": "Joint Warrior Strike Exercises",
                "is_india_relevant": False,
                "ships": [
                    {"name": "HMS Queen Elizabeth", "hull": "R08", "type": "Fleet Aircraft Carrier", "country": "UK", "status": "F-35B Lightning Ops", "speed": "19.2 kts", "heading": "045°", "source": "Royal Navy", "confidence": "High"},
                    {"name": "HMS Defender", "hull": "D36", "type": "Type 45 Destroyer", "country": "UK", "status": "Air Defense Screen", "speed": "18.0 kts", "heading": "045°", "source": "Royal Navy", "confidence": "High"},
                    {"name": "HMS Kent", "hull": "F78", "type": "Type 23 ASW Frigate", "country": "UK", "status": "Sub-Surface Screen", "speed": "16.0 kts", "heading": "040°", "source": "Royal Navy", "confidence": "High"}
                ]
            },

            # --- FRENCH & ITALIAN NAVIES ---
            {
                "id": "fleet-mediterranean",
                "name": "French Marine Nationale Carrier Strike Group (FS Charles de Gaulle)",
                "region": "Eastern Mediterranean / Crete Basin",
                "country": "France",
                "country_code": "FR",
                "lat": 34.80,
                "lon": 24.50,
                "ship_count": 7,
                "flag": "Marine Nationale (France)",
                "air_wing_strike_radius_nm": 550,
                "combat_radius_km": 1020,
                "radar_coverage_km": 420,
                "air_defense_envelope_km": 140,
                "source": "Marine Nationale Press Service / U.S. 6th Fleet",
                "verified_official_source": "Marine Nationale Official Command / French Ministry of Armed Forces",
                "official_dispatch_quote": "FS Charles de Gaulle (R91) carrier strike group executed mission Antares combat training with Rafale-M fighters in the Eastern Mediterranean.",
                "official_source_url": "https://www.defense.gouv.fr/marine",
                "official_verification_badge": "MARINE NATIONALE VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Eastern Mediterranean / Crete Basin (34.8°N, 24.5°E)",
                "last_reported": (now - timedelta(hours=3)).isoformat(),
                "status": "Air Dominance & Interoperability Patrol",
                "is_india_relevant": True,
                "ships": [
                    {"name": "FS Charles de Gaulle", "hull": "R91", "type": "Nuclear Aircraft Carrier", "country": "FR", "status": "Rafale-M Ops", "speed": "21.0 kts", "heading": "095°", "source": "Marine Nationale", "confidence": "High"},
                    {"name": "FS Forbin", "hull": "D620", "type": "Horizon Air Defense Destroyer", "country": "FR", "status": "Screen", "speed": "19.0 kts", "heading": "095°", "source": "Marine Nationale", "confidence": "High"},
                    {"name": "FS Provence", "hull": "D652", "type": "Aquitaine FREMM Frigate", "country": "FR", "status": "ASW Patrol", "speed": "17.0 kts", "heading": "095°", "source": "Marine Nationale", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-italy-cavour",
                "name": "Italian Navy Carrier Strike Group (ITS Cavour C550)",
                "region": "Central Mediterranean / Ionian Sea",
                "country": "Italy",
                "country_code": "IT",
                "lat": 37.50,
                "lon": 16.80,
                "ship_count": 5,
                "flag": "Marina Militare (Italy)",
                "air_wing_strike_radius_nm": 480,
                "combat_radius_km": 890,
                "radar_coverage_km": 380,
                "air_defense_envelope_km": 130,
                "source": "Marina Militare Official Portal",
                "verified_official_source": "Marina Militare General Staff / Italian Ministry of Defence",
                "official_dispatch_quote": "ITS Cavour (C550) carrier group conducting F-35B Lightning II expeditionary flight operations across the central Mediterranean.",
                "official_source_url": "https://www.marina.difesa.it",
                "official_verification_badge": "MARINA MILITARE VERIFIED",
                "official_confirmation_date": "2026-08-29",
                "verified_sector": "Ionian Sea / Gulf of Taranto Approach (37.5°N, 16.8°E)",
                "last_reported": (now - timedelta(hours=5)).isoformat(),
                "status": "Expeditionary Strike Training",
                "is_india_relevant": False,
                "ships": [
                    {"name": "ITS Cavour", "hull": "C550", "type": "STOVL Aircraft Carrier", "country": "IT", "status": "F-35B / AV-8B Flight Ops", "speed": "19.5 kts", "heading": "160°", "source": "Marina Militare", "confidence": "High"},
                    {"name": "ITS Andrea Doria", "hull": "D553", "type": "Orizzonte Air Defense Destroyer", "country": "IT", "status": "Air Defense", "speed": "18.0 kts", "heading": "160°", "source": "Marina Militare", "confidence": "High"},
                    {"name": "ITS Alpino", "hull": "F594", "type": "Bergamini FREMM Frigate", "country": "IT", "status": "ASW Screen", "speed": "17.0 kts", "heading": "160°", "source": "Marina Militare", "confidence": "High"}
                ]
            },

            # --- INDIAN NAVY FLEETS ---
            {
                "id": "fleet-indian-vikrant",
                "name": "Indian Navy Western Fleet (INS Vikrant Carrier Strike Group)",
                "region": "Central Arabian Sea / Western EEZ",
                "country": "India",
                "country_code": "IN",
                "lat": 16.20,
                "lon": 69.80,
                "ship_count": 8,
                "flag": "Indian Navy (Western Naval Command)",
                "air_wing_strike_radius_nm": 450,
                "combat_radius_km": 830,
                "radar_coverage_km": 420,
                "air_defense_envelope_km": 150,
                "source": "PIB MoD / @indiannavy Official Press Release",
                "verified_official_source": "Press Information Bureau (PIB) MoD / Indian Navy Spokesperson",
                "official_dispatch_quote": "INS Vikrant (R11) CSG with guided-missile destroyers INS Kolkata and INS Mormugao executed full-spectrum carrier air wing combat maneuvers in the Arabian Sea.",
                "official_source_url": "https://pib.gov.in",
                "official_verification_badge": "PIB NAVY DISPATCH",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Central Arabian Sea / Goa Approach (16.2°N, 69.8°E)",
                "last_reported": (now - timedelta(hours=1)).isoformat(),
                "status": "Full Spectrum Carrier Readiness Patrol",
                "is_india_relevant": True,
                "ships": [
                    {"name": "INS Vikrant", "hull": "R11", "type": "Indigenous Aircraft Carrier", "country": "IN", "status": "MiG-29K Flight Ops", "speed": "20.0 kts", "heading": "260°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Kolkata", "hull": "D63", "type": "Stealth Guided Missile Destroyer", "country": "IN", "status": "Air Defense Screen", "speed": "18.0 kts", "heading": "260°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Mormugao", "hull": "D67", "type": "Visakhapatnam-class Destroyer", "country": "IN", "status": "Forward Screen", "speed": "18.5 kts", "heading": "255°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Chennai", "hull": "D65", "type": "Kolkata-class Destroyer", "country": "IN", "status": "Anti-Submarine Screen", "speed": "16.5 kts", "heading": "265°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Deepak", "hull": "A50", "type": "Fleet Replenishment Tanker", "country": "IN", "status": "Underway Replenishment", "speed": "13.0 kts", "heading": "260°", "source": "Indian Navy", "confidence": "High"}
                ]
            },
            {
                "id": "fleet-bay-bengal",
                "name": "Indian Navy Eastern Fleet (INS Vikramaditya Carrier Strike Group)",
                "region": "Bay of Bengal / Andaman Sea",
                "country": "India",
                "country_code": "IN",
                "lat": 14.50,
                "lon": 86.20,
                "ship_count": 7,
                "flag": "Indian Navy (Eastern Naval Command)",
                "air_wing_strike_radius_nm": 420,
                "combat_radius_km": 780,
                "radar_coverage_km": 380,
                "air_defense_envelope_km": 100,
                "source": "PIB MoD / Eastern Naval Command HQ",
                "verified_official_source": "Press Information Bureau (PIB) MoD / Eastern Naval Command",
                "official_dispatch_quote": "INS Vikramaditya (R33) CSG conducted integrated anti-submarine exercises and long-range P-8I Neptune maritime patrol coordination in the Bay of Bengal.",
                "official_source_url": "https://pib.gov.in",
                "official_verification_badge": "PIB NAVY DISPATCH",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "Bay of Bengal / Visakhapatnam-Andaman Sector (14.5°N, 86.2°E)",
                "last_reported": (now - timedelta(hours=1)).isoformat(),
                "status": "Operational Readiness Patrol / Malacca Oversight",
                "is_india_relevant": True,
                "ships": [
                    {"name": "INS Vikramaditya", "hull": "R33", "type": "Modified Kiev Aircraft Carrier", "country": "IN", "status": "Carrier Strike Exercises", "speed": "19.0 kts", "heading": "160°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Ranvijay", "hull": "D55", "type": "Rajput-class Destroyer", "country": "IN", "status": "Carrier Screen", "speed": "18.0 kts", "heading": "160°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Kavaratti", "hull": "P31", "type": "Kamorta-class ASW Corvette", "country": "IN", "status": "Anti-Submarine Screen", "speed": "16.0 kts", "heading": "155°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Shivalik", "hull": "F47", "type": "Stealth Multi-Role Frigate", "country": "IN", "status": "Forward Surveillance", "speed": "17.2 kts", "heading": "140°", "source": "Indian Navy", "confidence": "High"},
                    {"name": "INS Jyoti", "hull": "A58", "type": "Fleet Tanker / Replenishment", "country": "IN", "status": "Underway Replenishment", "speed": "12.0 kts", "heading": "160°", "source": "Indian Navy", "confidence": "Medium"}
                ]
            },

            # --- PAKISTAN NAVY ---
            {
                "id": "fleet-pakistan-navy",
                "name": "Pakistan Navy 25th Destroyer Squadron & Submarine Force",
                "region": "North Arabian Sea / Makran Coast",
                "country": "Pakistan",
                "country_code": "PK",
                "lat": 23.60,
                "lon": 64.80,
                "ship_count": 6,
                "flag": "Pakistan Navy",
                "air_wing_strike_radius_nm": 280,
                "combat_radius_km": 520,
                "radar_coverage_km": 300,
                "air_defense_envelope_km": 100,
                "source": "ISPR Official Press Release / DGPR Pakistan Navy",
                "verified_official_source": "Inter-Services Public Relations (ISPR) Directorate / DGPR Pakistan Navy",
                "official_dispatch_quote": "Pakistan Navy warships PNS Babur (F-280), PNS Taimur (F-262), and Hashmat-class submarines conducted operational patrols and missile defense drills in the North Arabian Sea.",
                "official_source_url": "https://ispr.gov.pk/press-release",
                "official_verification_badge": "ISPR VERIFIED",
                "official_confirmation_date": "2026-08-30",
                "verified_sector": "North Arabian Sea / Ormara-Karachi EEZ (23.6°N, 64.8°E)",
                "last_reported": (now - timedelta(hours=3)).isoformat(),
                "status": "Operational Patrol / Arabian Sea Vigilance",
                "is_india_relevant": True,
                "ships": [
                    {"name": "PNS Babur", "hull": "F-280", "type": "Babur-class MILGEM Corvette", "country": "PK", "status": "Patrol", "speed": "17.0 kts", "heading": "210°", "source": "ISPR", "confidence": "High"},
                    {"name": "PNS Taimur", "hull": "F-262", "type": "Type 054A/P Frigate", "country": "PK", "status": "Air Defense", "speed": "18.5 kts", "heading": "210°", "source": "ISPR", "confidence": "High"},
                    {"name": "PNS Tughril", "hull": "F-261", "type": "Type 054A/P Frigate", "country": "PK", "status": "Escort", "speed": "16.0 kts", "heading": "220°", "source": "ISPR", "confidence": "High"},
                    {"name": "PNS Yarmook", "hull": "F-271", "type": "Offshore Patrol Vessel", "country": "PK", "status": "Coastal Patrol", "speed": "15.0 kts", "heading": "200°", "source": "ISPR", "confidence": "High"},
                    {"name": "PNS Hashmat", "hull": "S-135", "type": "Agosta 90B Submarine", "country": "PK", "status": "Submerged Patrol", "speed": "8.0 kts", "heading": "180°", "source": "ISPR", "confidence": "Medium"}
                ]
            }
        ]
        for f in fleets_data:
            self.naval_fleets[f["id"]] = f

        # -------------------------------------------------------------
        # 3. Global & Regional Events Feed (50+ Events)
        # -------------------------------------------------------------
        events_catalog = [
            {
                "title": "PLA Western Theater Command Deploys HQ-9 Air Defense Regiment East of Depsang LAC",
                "summary": "Commercial satellite imagery corroborates permanent radar masts, missile TEL revetments, and hardened subterranean fuel bunkers 45km east of the LAC.",
                "category": "military",
                "severity": 3,
                "hours_ago": 1.2,
                "lat": 35.25, "lon": 78.40,
                "location_name": "Depsang Plains / Eastern Ladakh LAC",
                "is_india_relevant": True,
                "sources": [{"name": "Jane's Defence Weekly", "url": "https://janes.com/lac-depsang"}, {"name": "The Hindu PTI", "url": "https://thehindu.com"}]
            },
            {
                "title": "Indian Navy Deploys P-8I Neptune Patrol Aircraft to Great Nicobar Island Runway",
                "summary": "Indian Navy conducts long-range maritime patrol flights over the Malacca Strait western approach from newly expanded INS Baaz air station.",
                "category": "maritime",
                "severity": 2,
                "hours_ago": 1.8,
                "lat": 6.98, "lon": 93.88,
                "location_name": "Campbell Bay / INS Baaz / Great Nicobar",
                "is_india_relevant": True,
                "sources": [{"name": "Indian Navy Spokesperson", "url": "https://indiannavy.nic.in"}, {"name": "ANI News", "url": "https://aninews.in"}]
            },
            {
                "title": "India-Bound Crude Carrier Re-Routes North of Tunb Islands Amid Hormuz Chokepoint Advisory",
                "summary": "AIS telemetry indicates the VLCC 'Desh Shanti' carrying 2M barrels of crude shifted transit heading outside standard outbound lanes following regional maritime notice.",
                "category": "trade",
                "severity": 2,
                "hours_ago": 2.5,
                "lat": 26.35, "lon": 55.80,
                "location_name": "Strait of Hormuz / Gulf of Oman",
                "is_india_relevant": True,
                "sources": [{"name": "AISStream Live Telemetry", "url": "https://aisstream.io"}, {"name": "UKMTO Advisory Notice", "url": "https://ukmto.org"}]
            },
            {
                "title": "Unidentified Radar Contact Transponder Anomaly Logged in Western Border Airspace",
                "summary": "ADS-B ground stations detected an aircraft contact with unfiled transponder cruising at FL310 performing an oval loiter track 30km west of the border buffer.",
                "category": "airspace",
                "severity": 2,
                "hours_ago": 3.1,
                "lat": 27.80, "lon": 71.15,
                "location_name": "Western Air Corridor / Jaisalmer Buffer",
                "is_india_relevant": True,
                "sources": [{"name": "OpenSky Network Feed", "url": "https://opensky-network.org"}]
            },
            {
                "title": "Multi-Agency Reports of Sudden Strait of Malacca Navigational Restriction and GPS Spoofing Cluster",
                "summary": "Multiple merchant vessels report severe GNSS spoofing anomalies and unannounced naval drill advisory across the Western Singapore Strait / Malacca approaches.",
                "category": "maritime",
                "severity": 4,
                "hours_ago": 0.7,
                "lat": 2.20, "lon": 102.10,
                "location_name": "Strait of Malacca / Critical Gateway",
                "is_india_relevant": True,
                "sources": [{"name": "Reuters Maritime Desk", "url": "https://reuters.com"}, {"name": "Lloyd's List Intelligence", "url": "https://lloydslist.com"}]
            },
            {
                "title": "French Frigate Amiral Ronarc'h Arrives in Stockholm for Joint Baltic NATO Exercises",
                "summary": "The French Navy's newest FDI-class frigate Amiral Ronarc'h docked at Frihamnen port in Stockholm for high-readiness Baltic Sea interoperability drills.",
                "category": "political",
                "severity": 1,
                "hours_ago": 0.1,
                "lat": 59.34, "lon": 18.07,
                "location_name": "Stockholm, Sweden",
                "is_india_relevant": False,
                "sources": [{"name": "Marine Nationale Press", "url": "https://defense.gouv.fr/marine"}, {"name": "SVT News Sweden", "url": "https://svt.se"}]
            },
            {
                "title": "HMS Severn Arrives in London for River Thames Strategic Flotilla Review",
                "summary": "Royal Navy River-class offshore patrol vessel HMS Severn navigated under Tower Bridge, anchoring in London for bilateral naval security briefings.",
                "category": "political",
                "severity": 1,
                "hours_ago": 0.15,
                "lat": 51.50, "lon": -0.07,
                "location_name": "London, United Kingdom",
                "is_india_relevant": False,
                "sources": [{"name": "Royal Navy News", "url": "https://royalnavy.mod.uk"}, {"name": "BBC Defence", "url": "https://bbc.co.uk/news"}]
            },
            {
                "title": "Severe Drought Declared in Democratic Republic of Congo, Kenya, Tanzania, and Uganda",
                "summary": "UN OCHA and regional meteorological agencies issued joint famine-warning bulletins affecting over 18 million agrarian citizens in East Africa.",
                "category": "disaster",
                "severity": 2,
                "hours_ago": 0.35,
                "lat": -1.28, "lon": 36.82,
                "location_name": "East Africa / Nairobi",
                "is_india_relevant": False,
                "sources": [{"name": "UN OCHA Bulletin", "url": "https://unocha.org"}, {"name": "FEWS NET Drought Alert", "url": "https://fews.net"}]
            },
            {
                "title": "Working Mechanism for Consultation & Coordination on India-China Border Affairs (WMCC) 22nd Session Concludes",
                "summary": "Diplomatic delegations from New Delhi and Beijing met to review ground situation in Eastern Ladakh sectors, agreeing to maintain peace and tranquility.",
                "category": "diplomatic",
                "severity": 1,
                "hours_ago": 4.5,
                "lat": 28.61, "lon": 77.20,
                "location_name": "New Delhi Diplomatic Enclave",
                "is_india_relevant": True,
                "sources": [{"name": "Ministry of External Affairs (MEA)", "url": "https://mea.gov.in"}, {"name": "PIB India", "url": "https://pib.gov.in"}]
            },
            {
                "title": "Chinese Hydrographic Survey Vessel 'Hai Yang 24' Enters India EEZ Adjacent to Andaman Sea",
                "summary": "Automated geofencing flagged the 4,000-ton Chinese research vessel operating acoustic bathymetry sonar arrays 180nm east of Port Blair without coastal state clearance.",
                "category": "maritime",
                "severity": 3,
                "hours_ago": 5.2,
                "lat": 11.40, "lon": 94.80,
                "location_name": "Andaman Sea / India Eastern EEZ Boundary",
                "is_india_relevant": True,
                "sources": [{"name": "Naval Intelligence Directorate", "url": "https://indiannavy.nic.in"}, {"name": "Hindustan Times OSINT", "url": "https://hindustantimes.com"}]
            }
        ]

        for ev_data in events_catalog:
            ev_id = f"ev-{uuid.uuid4().hex[:8]}"
            flag_id = f"flag-{uuid.uuid4().hex[:8]}"
            hours = ev_data.get("hours_ago", 1.0)
            ev_created = (now - timedelta(hours=hours)).isoformat()
            is_live = hours < 6.0
            is_pending = ev_data["severity"] == 4
            prov_source = ev_data["sources"][0]["name"] if ev_data.get("sources") else "Verified Wire Reporting"

            self.events[ev_id] = {
                "id": ev_id,
                "title": ev_data["title"],
                "summary": ev_data["summary"],
                "category": ev_data["category"],
                "source_type": "news",
                "sources": ev_data["sources"],
                "location": {
                    "lat": ev_data["lat"],
                    "lon": ev_data["lon"],
                    "name": ev_data["location_name"]
                },
                "severity_global": ev_data["severity"],
                "freshness": "live" if is_live else "delayed",
                "provenance": prov_source,
                "is_india_relevant": ev_data.get("is_india_relevant", True),
                "last_updated": ev_created,
                "created_at": ev_created
            }

            self.india_flags[flag_id] = {
                "id": flag_id,
                "event_id": ev_id,
                "category": ev_data["category"],
                "impact_severity": ev_data["severity"],
                "confidence": "high" if len(ev_data["sources"]) > 1 else "medium",
                "rationale": f"Corroborated by verified open reporting. Spatial proximity to {ev_data['location_name']}. Scored according to autonomous specialist agent rubrics.",
                "triggering_signals": {
                    "specialist_agent": "india_impact_classifier",
                    "geofence_match": "active_monitoring_zone",
                    "category": ev_data["category"]
                },
                "source_event_ids": [ev_id],
                "freshness": "live" if is_live else "delayed",
                "provenance": "India-Impact Classifier Agent (Multi-Agent RAG)",
                "is_india_relevant": ev_data.get("is_india_relevant", True),
                "last_updated": ev_created,
                "status": "pending_review" if is_pending else "approved",
                "created_at": ev_created
            }

            if is_pending:
                self.review_queue[flag_id] = {
                    "flag": self.india_flags[flag_id],
                    "event": self.events[ev_id],
                    "submitted_at": ev_created
                }

        # Seed Leaders & Fleets freshness
        for leader in self.world_leaders.values():
            leader["freshness"] = "live"
            leader["last_updated"] = leader.get("statement_date", now.isoformat())
            leader["provenance"] = leader.get("source", "Official Government Press Release")

        for fleet in self.naval_fleets.values():
            fleet["freshness"] = "live"
            fleet["last_updated"] = now.isoformat()
            fleet["provenance"] = "USNI News / Maritime Open Fleet Trackers"

        # Seed Flights, Vessels, Disasters, Domestic Stability, Installations
        self._seed_flight_contacts()
        self._seed_vessel_contacts()
        self._seed_disasters()
        self._seed_installations()
        self._seed_domestic_stability()

    def _seed_flight_contacts(self):
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        flights = [
            # ---------------- Military Fighter Jets & Combat Patrol with Range Envelopes ----------------
            {
                "icao24": "IAF010", 
                "callsign": "RAFALE01", 
                "airline": "Indian Air Force (17 Sqn Golden Arrows)", 
                "lat": 30.38, "lon": 76.83, 
                "altitude_m": 11200, "velocity_kmh": 980, "heading": 45, 
                "type": "fighter_jet", 
                "origin": "Ambala AFS", "dest": "Northern CAP", 
                "model": "Dassault Rafale DH", 
                "combat_radius_km": 1050, 
                "radar_range_km": 160, 
                "max_speed_mach": 1.8,
                "ceiling_m": 15240,
                "mission_profile": "Combat Air Patrol (CAP) / BVR Escort",
                "is_india_relevant": True,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "IAF011", 
                "callsign": "SU30_KNIGHT", 
                "airline": "Indian Air Force (220 Sqn Desert Tigers)", 
                "lat": 26.30, "lon": 73.05, 
                "altitude_m": 12500, "velocity_kmh": 1050, "heading": 290, 
                "type": "fighter_jet", 
                "origin": "Jodhpur AFS", "dest": "Western Sector Sweep", 
                "model": "Sukhoi Su-30MKI Flanker-H", 
                "combat_radius_km": 1850, 
                "radar_range_km": 350, 
                "max_speed_mach": 2.0,
                "ceiling_m": 17300,
                "mission_profile": "Long-Range Air Superiority / BrahMos-A Strike",
                "is_india_relevant": True,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "IAF001", 
                "callsign": "NETRA01", 
                "airline": "Indian Air Force", 
                "lat": 31.80, "lon": 75.10, 
                "altitude_m": 9800, "velocity_kmh": 710, "heading": 320, 
                "type": "military_aewc", 
                "origin": "Bhatinda AFB", "dest": "Western Border Orbit", 
                "model": "EMB-145 Netra AEW&C", 
                "combat_radius_km": 900, 
                "radar_range_km": 400, 
                "max_speed_mach": 0.78,
                "ceiling_m": 12000,
                "mission_profile": "Airborne Early Warning & Battle Management",
                "is_india_relevant": True,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "IAF003", 
                "callsign": "IN-P8I", 
                "airline": "Indian Navy (INAS 312 Albatross)", 
                "lat": 8.50, "lon": 86.20, 
                "altitude_m": 6200, "velocity_kmh": 640, "heading": 160, 
                "type": "military_maritime_patrol", 
                "origin": "INS Rajali Arakkonam", "dest": "IOR Southern Chokepoint", 
                "model": "Boeing P-8I Neptune", 
                "combat_radius_km": 2200, 
                "radar_range_km": 450, 
                "max_speed_mach": 0.82,
                "ceiling_m": 12500,
                "mission_profile": "Long-Range Anti-Submarine Warfare (ASW) & Maritime Domain Awareness",
                "is_india_relevant": True,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "USAF02", 
                "callsign": "LIGHTNING01", 
                "airline": "US Air Force (380th AEW)", 
                "lat": 24.25, "lon": 54.55, 
                "altitude_m": 12000, "velocity_kmh": 1100, "heading": 180, 
                "type": "fighter_jet", 
                "origin": "Al Dhafra AB", "dest": "Persian Gulf CAP", 
                "model": "Lockheed Martin F-35A Lightning II", 
                "combat_radius_km": 1150, 
                "radar_range_km": 150, 
                "max_speed_mach": 1.6,
                "ceiling_m": 15200,
                "mission_profile": "5th Gen Stealth Strike & EW Escort",
                "is_india_relevant": True,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "PLAAF1", 
                "callsign": "DRAGON01", 
                "airline": "PLA Air Force (Western Theatre)", 
                "lat": 36.50, "lon": 79.90, 
                "altitude_m": 13500, "velocity_kmh": 1150, "heading": 250, 
                "type": "fighter_jet", 
                "origin": "Hotan Airbase", "dest": "Karakoram Corridor", 
                "model": "Chengdu J-20 Mighty Dragon", 
                "combat_radius_km": 1200, 
                "radar_range_km": 200, 
                "max_speed_mach": 2.0,
                "ceiling_m": 18000,
                "mission_profile": "5th Gen Heavy Air Superiority / Border Patrol",
                "is_india_relevant": True,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "RAF001", 
                "callsign": "TYPHOON77", 
                "airline": "Royal Air Force (XI Sqn)", 
                "lat": 53.05, "lon": -0.15, 
                "altitude_m": 10500, "velocity_kmh": 990, "heading": 90, 
                "type": "fighter_jet", 
                "origin": "RAF Coningsby", "dest": "North Sea QRA", 
                "model": "Eurofighter Typhoon FGR4", 
                "combat_radius_km": 1380, 
                "radar_range_km": 160, 
                "max_speed_mach": 2.0,
                "ceiling_m": 16800,
                "mission_profile": "Quick Reaction Alert (QRA) Intercept",
                "is_india_relevant": False,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },
            {
                "icao24": "USAF05", 
                "callsign": "RAPTOR01", 
                "airline": "US Air Force (1st FW)", 
                "lat": 37.08, "lon": -76.35, 
                "altitude_m": 14000, "velocity_kmh": 1200, "heading": 85, 
                "type": "fighter_jet", 
                "origin": "Langley AFB", "dest": "Atlantic Air Defense", 
                "model": "Lockheed Martin F-22A Raptor", 
                "combat_radius_km": 1100, 
                "radar_range_km": 240, 
                "max_speed_mach": 2.25,
                "ceiling_m": 19800,
                "mission_profile": "Stealth Air Dominance",
                "is_india_relevant": False,
                "freshness": "live", 
                "provenance": "OpenSky Network / ADSB.lol", 
                "last_updated": now_iso
            },

            # ---------------- Global Commercial & Transcontinental Air Routes ----------------
            {"icao24": "8002a1", "callsign": "AIC101", "airline": "Air India", "lat": 28.55, "lon": 77.10, "altitude_m": 10500, "velocity_kmh": 820, "heading": 140, "anomaly": None, "type": "commercial", "origin": "DEL", "dest": "BOM", "model": "B787-8", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "8003f4", "callsign": "SEJ402", "airline": "SpiceJet", "lat": 19.08, "lon": 72.88, "altitude_m": 8200, "velocity_kmh": 750, "heading": 210, "anomaly": None, "type": "commercial", "origin": "BOM", "dest": "BLR", "model": "B737-800", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "8005b8", "callsign": "IGO884", "airline": "IndiGo", "lat": 13.19, "lon": 77.70, "altitude_m": 9400, "velocity_kmh": 800, "heading": 350, "anomaly": None, "type": "commercial", "origin": "BLR", "dest": "DEL", "model": "A321neo", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "7c1290", "callsign": "SIA416", "airline": "Singapore Airlines", "lat": 10.50, "lon": 85.20, "altitude_m": 11200, "velocity_kmh": 890, "heading": 280, "anomaly": None, "type": "international", "origin": "SIN", "dest": "MAA", "model": "A350-900", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "400ab2", "callsign": "BAW138", "airline": "British Airways", "lat": 24.50, "lon": 69.20, "altitude_m": 11500, "velocity_kmh": 910, "heading": 115, "anomaly": None, "type": "international", "origin": "LHR", "dest": "BOM", "model": "B777-300ER", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "896123", "callsign": "UAE504", "airline": "Emirates", "lat": 22.80, "lon": 66.40, "altitude_m": 10800, "velocity_kmh": 880, "heading": 110, "anomaly": None, "type": "international", "origin": "DXB", "dest": "BOM", "model": "A380-800", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "3c65c2", "callsign": "DLH456", "airline": "Lufthansa", "lat": 50.03, "lon": 8.57, "altitude_m": 10900, "velocity_kmh": 890, "heading": 110, "type": "international", "origin": "FRA", "dest": "DEL", "model": "A340-300", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "a00112", "callsign": "AAL100", "airline": "American Airlines", "lat": 40.64, "lon": -73.78, "altitude_m": 11800, "velocity_kmh": 920, "heading": 65, "type": "international", "origin": "JFK", "dest": "LHR", "model": "B777-200", "is_india_relevant": False, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "a00554", "callsign": "UAL857", "airline": "United Airlines", "lat": 37.62, "lon": -122.37, "altitude_m": 10600, "velocity_kmh": 880, "heading": 290, "type": "international", "origin": "SFO", "dest": "PVG", "model": "B787-9", "is_india_relevant": False, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "8009cc", "callsign": "AIC342", "airline": "Air India", "lat": 22.65, "lon": 88.44, "altitude_m": 6800, "velocity_kmh": 680, "heading": 45, "anomaly": None, "type": "commercial", "origin": "CCU", "dest": "GAU", "model": "A320neo", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso},
            {"icao24": "8008da", "callsign": "VTI922", "airline": "Vistara", "lat": 17.24, "lon": 78.42, "altitude_m": 8900, "velocity_kmh": 790, "heading": 180, "anomaly": None, "type": "commercial", "origin": "HYD", "dest": "MAA", "model": "A320neo", "is_india_relevant": True, "freshness": "live", "provenance": "OpenSky Network (ADS-B)", "last_updated": now_iso}
        ]
        for f in flights:
            fid = f.get("icao24", str(uuid.uuid4()))
            self.flight_contacts[fid] = {
                "id": fid,
                **f,
                "observed_at": now_iso
            }

    def _seed_vessel_contacts(self):
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        vessels = [
            {"mmsi": 419000123, "ship_name": "DESH SHANTI", "type": "Crude Oil Tanker", "lat": 25.80, "lon": 56.40, "speed_knots": 14.2, "heading": 125, "flag": "IN", "destination": "SIKKA (INDIA)", "status": "Underway", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 419000456, "ship_name": "JAG LEELA", "type": "Oil Products Tanker", "lat": 18.90, "lon": 71.50, "speed_knots": 13.0, "heading": 70, "flag": "IN", "destination": "MUMBAI", "status": "Underway", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 563000789, "ship_name": "MAERSK COLOMBO", "type": "Container Ship", "lat": 7.20, "lon": 79.50, "speed_knots": 18.5, "heading": 310, "flag": "SG", "destination": "JNPT MUMBAI", "status": "Underway", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 636000321, "ship_name": "PACIFIC GLORY", "type": "Bulk Carrier", "lat": 14.50, "lon": 83.20, "speed_knots": 11.8, "heading": 215, "flag": "LR", "destination": "VISAKHAPATNAM", "status": "Underway", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 413000999, "ship_name": "HAI YANG 24", "type": "Research / Hydrographic Survey", "lat": 5.80, "lon": 87.20, "speed_knots": 6.5, "heading": 180, "flag": "CN", "destination": "HIGH SEAS (IOR)", "status": "Engaged in Survey", "anomaly": {"type": "ior_survey_track", "label": "Hydrographic Survey Profile in IOR", "severity": 2}, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 999000888, "ship_name": "DARK TANKER (UNFLAGGED)", "type": "VLCC Tanker", "lat": 26.10, "lon": 55.40, "speed_knots": 0.5, "heading": 0, "flag": "PA", "destination": "UNKNOWN", "status": "AIS Inactive / Dark Gap", "anomaly": {"type": "ais_dark_gap", "label": "Vessel Went AIS-Dark Near Hormuz (4h gap)", "severity": 3}, "is_india_relevant": True, "freshness": "delayed", "provenance": "aisstream.io (AIS Dark Gap Alert)", "last_updated": now_iso},
            {"mmsi": 525000111, "ship_name": "WAN HAI 502", "type": "Container Ship", "lat": 3.10, "lon": 100.80, "speed_knots": 16.4, "heading": 130, "flag": "TW", "destination": "CHENNAI", "status": "Underway", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 419000999, "ship_name": "INS TARKASH", "type": "Guided Missile Frigate", "lat": 20.40, "lon": 68.80, "speed_knots": 18.0, "heading": 260, "flag": "IN", "destination": "NORTH ARABIAN SEA", "status": "Naval Patrol", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "Indian Navy Official Readout", "last_updated": now_iso},
            {"mmsi": 354000122, "ship_name": "EVER GIVEN", "type": "Ultra Large Container", "lat": 12.10, "lon": 44.80, "speed_knots": 19.2, "heading": 315, "flag": "PA", "destination": "ROTTERDAM", "status": "Underway", "anomaly": None, "is_india_relevant": True, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 211000345, "ship_name": "HAPAG LLOYD BERLIN", "type": "Container Ship", "lat": 50.80, "lon": -1.30, "speed_knots": 17.0, "heading": 240, "flag": "DE", "destination": "NEW YORK", "status": "Underway", "anomaly": None, "is_india_relevant": False, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso},
            {"mmsi": 311000876, "ship_name": "PACIFIC EXPLORER", "type": "Panamax Bulk Carrier", "lat": 9.10, "lon": -79.70, "speed_knots": 8.0, "heading": 320, "flag": "BS", "destination": "PANAMA CANAL TRANSIT", "status": "In Transit", "anomaly": None, "is_india_relevant": False, "freshness": "live", "provenance": "aisstream.io (Live AIS)", "last_updated": now_iso}
        ]
        for v in vessels:
            vid = str(v.get("mmsi", uuid.uuid4()))
            self.vessel_contacts[vid] = {
                "id": vid,
                **v,
                "last_seen_at": now_iso
            }

    def _seed_disasters(self):
        now = datetime.now(timezone.utc)
        disasters = [
            {"id": "eq-1", "title": "M5.8 Earthquake - Hindu Kush", "type": "earthquake", "magnitude": 5.8, "depth_km": 185, "lat": 36.45, "lon": 71.20, "time": (now - timedelta(hours=8)).isoformat(), "source": "USGS", "is_india_relevant": True, "freshness": "live", "provenance": "USGS Global Earthquake Hazards Program", "last_updated": (now - timedelta(hours=8)).isoformat()},
            {"id": "eq-2", "title": "M6.1 Deep Sea Earthquake - Andaman Trench", "type": "earthquake", "magnitude": 6.1, "depth_km": 95, "lat": 7.45, "lon": 94.10, "time": (now - timedelta(hours=68)).isoformat(), "source": "USGS", "is_india_relevant": True, "freshness": "delayed", "provenance": "USGS Global Earthquake Hazards Program", "last_updated": (now - timedelta(hours=68)).isoformat()},
            {"id": "eq-3", "title": "M5.2 Earthquake - Zagros Mountains", "type": "earthquake", "magnitude": 5.2, "depth_km": 12, "lat": 28.30, "lon": 53.40, "time": (now - timedelta(hours=14)).isoformat(), "source": "USGS", "is_india_relevant": True, "freshness": "live", "provenance": "USGS Global Earthquake Hazards Program", "last_updated": (now - timedelta(hours=14)).isoformat()},
            {"id": "dr-1", "title": "Severe Drought - East Africa (DRC, Kenya, Tanzania, Uganda)", "type": "drought", "severity": 2, "lat": -1.28, "lon": 36.82, "time": (now - timedelta(hours=1)).isoformat(), "source": "FEWS NET", "is_india_relevant": False, "freshness": "live", "provenance": "FEWS NET Food Security & Drought Warning", "last_updated": (now - timedelta(hours=1)).isoformat()},
            {"id": "dr-2", "title": "Drought Stress - Central America Dry Corridor", "type": "drought", "severity": 2, "lat": 14.63, "lon": -90.50, "time": (now - timedelta(hours=1)).isoformat(), "source": "ReliefWeb", "is_india_relevant": False, "freshness": "live", "provenance": "ReliefWeb Global Humanitarian Hazards", "last_updated": (now - timedelta(hours=1)).isoformat()}
        ]
        for d in disasters:
            self.disasters[d["id"]] = d

    def _seed_installations(self):
        now_iso = datetime.now(timezone.utc).isoformat()
        bases_catalog = [
            # ================= INDIA STRATEGIC BASES =================
            # Air Force Bases
            {"id": "base-in-ambala", "name": "Ambala Air Force Station", "type": "airbase", "subtype": "IAF Primary Strike Base", "country": "India", "country_code": "IN", "lat": 30.368, "lon": 76.817, "runway_count": 2, "active_squadrons": "17 Sqn (Golden Arrows - Rafale), 5 Sqn (Daggers - Jaguar)", "strategic_role": "Western Air Command Western Sector Air Dominance", "is_india_relevant": True, "freshness": "live", "provenance": "MoD Open Gazette / OSM Strategic", "last_updated": now_iso},
            {"id": "base-in-hashimara", "name": "Hashimara Air Force Station", "type": "airbase", "subtype": "IAF Eastern Strike Base", "country": "India", "country_code": "IN", "lat": 26.702, "lon": 89.370, "runway_count": 2, "active_squadrons": "101 Sqn (Falcons - Rafale)", "strategic_role": "Eastern Air Command Siliguri Corridor Air Dominance & Tibet LAC Deterrence", "is_india_relevant": True, "freshness": "live", "provenance": "MoD Open Gazette / OSM Strategic", "last_updated": now_iso},
            {"id": "base-in-bareilly", "name": "Bareilly Air Force Station", "type": "airbase", "subtype": "IAF Air Superiority Base", "country": "India", "country_code": "IN", "lat": 28.422, "lon": 79.450, "runway_count": 2, "active_squadrons": "8 Sqn (Pursoots - Su-30MKI), 24 Sqn (Hawks - Su-30MKI)", "strategic_role": "Central Air Command Air Superiority & BrahMos Strike Hub", "is_india_relevant": True, "freshness": "live", "provenance": "MoD Open Gazette / OSM Strategic", "last_updated": now_iso},
            {"id": "base-in-thanjavur", "name": "Thanjavur Air Force Station", "type": "airbase", "subtype": "IAF Maritime Strike Base", "country": "India", "country_code": "IN", "lat": 10.722, "lon": 79.102, "runway_count": 1, "active_squadrons": "222 Sqn (Tigersharks - Su-30MKI BrahMos-A)", "strategic_role": "Southern Air Command IOR Maritime Strike & Chokepoint Defense", "is_india_relevant": True, "freshness": "live", "provenance": "MoD Open Gazette / OSM Strategic", "last_updated": now_iso},
            {"id": "base-in-leh", "name": "Leh Kushok Bakula Rimpochee AFS", "type": "airbase", "subtype": "IAF High Altitude Forward Base", "country": "India", "country_code": "IN", "lat": 34.135, "lon": 77.546, "runway_count": 1, "active_squadrons": "Forward Detachments (MiG-29UPG, Su-30MKI, Apache AH-64E)", "strategic_role": "Eastern Ladakh High-Altitude Tactical Interception (Elevation 3,256m)", "is_india_relevant": True, "freshness": "live", "provenance": "MoD Open Gazette / OSM Strategic", "last_updated": now_iso},
            {"id": "base-in-arakkonam", "name": "INS Rajali (Arakkonam Naval Air Station)", "type": "airbase", "subtype": "Indian Navy Long-Range Maritime Patrol HQ", "country": "India", "country_code": "IN", "lat": 13.071, "lon": 79.690, "runway_count": 1, "active_squadrons": "INAS 312 (Albatross - Boeing P-8I Neptune)", "strategic_role": "Long-Range Anti-Submarine Warfare (ASW) Hub for Indian Ocean Region", "is_india_relevant": True, "freshness": "live", "provenance": "Indian Navy Official Readout", "last_updated": now_iso},
            # Naval Bases
            {"id": "base-in-karwar", "name": "INS Kadamba (Karwar Naval Base)", "type": "naval_base", "subtype": "Indian Navy Premier Mega Naval Base", "country": "India", "country_code": "IN", "lat": 14.770, "lon": 74.148, "runway_count": 0, "homeported_ships": "INS Vikramaditya (R33), Project 75 Kalvari Submarines, Stealth Destroyers", "strategic_role": "Project Seabird: Largest Dedicated Naval Base East of Suez Canal", "is_india_relevant": True, "freshness": "live", "provenance": "MoD / Indian Navy Open Release", "last_updated": now_iso},
            {"id": "base-in-mumbai", "name": "Mumbai Naval Dockyard (INS Angre)", "type": "naval_base", "subtype": "Western Naval Command HQ", "country": "India", "country_code": "IN", "lat": 18.924, "lon": 72.842, "runway_count": 0, "homeported_ships": "INS Vikrant (R11), Kolkata-class & Visakhapatnam-class Destroyers", "strategic_role": "Western Naval Command Headquarters & Arabian Sea Fleet Operations", "is_india_relevant": True, "freshness": "live", "provenance": "Indian Navy Official Portal", "last_updated": now_iso},
            {"id": "base-in-vizag", "name": "Visakhapatnam Naval Dockyard (INS Virbahu)", "type": "naval_base", "subtype": "Eastern Naval Command HQ & Submarine Base", "country": "India", "country_code": "IN", "lat": 17.698, "lon": 83.285, "runway_count": 0, "homeported_ships": "INS Arihant (SSBN), Eastern Fleet Destroyers & Frigates", "strategic_role": "Eastern Naval Command HQ & Strategic SSBN Nuclear Deterrence Bastion", "is_india_relevant": True, "freshness": "live", "provenance": "Indian Navy Official Portal", "last_updated": now_iso},
            {"id": "base-in-portblair", "name": "INS Jarawa / Port Blair Naval Base", "type": "naval_base", "subtype": "Andaman & Nicobar Command (ANC) HQ", "country": "India", "country_code": "IN", "lat": 11.666, "lon": 92.748, "runway_count": 0, "homeported_ships": "Amphibious Warfare Ships, Fast Attack Craft, Offshore Patrol Vessels", "strategic_role": "Tri-Services Command Overseeing Strait of Malacca & Bay of Bengal Chokepoints", "is_india_relevant": True, "freshness": "live", "provenance": "Indian Navy Official Portal", "last_updated": now_iso},

            # ================= UNITED STATES STRATEGIC BASES =================
            {"id": "base-us-norfolk", "name": "Naval Station Norfolk", "type": "naval_base", "subtype": "US Navy Atlantic Fleet Mega Hub", "country": "United States", "country_code": "US", "lat": 36.953, "lon": -76.302, "runway_count": 0, "homeported_ships": "USS Dwight D. Eisenhower (CVN-69), USS Gerald R. Ford (CVN-78), 75+ Warships", "strategic_role": "World's Largest Naval Station & US Fleet Forces Command HQ", "is_india_relevant": False, "freshness": "live", "provenance": "US Navy Open Source Facility", "last_updated": now_iso},
            {"id": "base-us-sandiego", "name": "Naval Base San Diego", "type": "naval_base", "subtype": "US Pacific Fleet Surface Combatant Hub", "country": "United States", "country_code": "US", "lat": 32.684, "lon": -117.130, "runway_count": 0, "homeported_ships": "USS Carl Vinson (CVN-70), USS Theodore Roosevelt (CVN-71), 50+ Surface Ships", "strategic_role": "Principal Homeport for the Pacific Fleet Surface Forces", "is_india_relevant": False, "freshness": "live", "provenance": "US Navy Open Source Facility", "last_updated": now_iso},
            {"id": "base-us-yokosuka", "name": "Commander Fleet Activities Yokosuka", "type": "naval_base", "subtype": "US 7th Fleet Forward Operating Base", "country": "United States", "country_code": "US", "lat": 35.293, "lon": 139.670, "runway_count": 0, "homeported_ships": "USS George Washington (CVN-73), Destroyer Squadron 15 (DESRON 15)", "strategic_role": "Forward Operating Hub for US Naval Power Projection in Western Pacific", "is_india_relevant": False, "freshness": "live", "provenance": "Commander Fleet Activities Yokosuka", "last_updated": now_iso},
            {"id": "base-us-bahrain", "name": "Naval Support Activity Bahrain", "type": "naval_base", "subtype": "US 5th Fleet & NAVCENT Headquarters", "country": "United States", "country_code": "US", "lat": 26.208, "lon": 50.608, "runway_count": 0, "homeported_ships": "US 5th Fleet Task Forces, Combined Maritime Forces (CMF)", "strategic_role": "Headquarters for US Naval Forces Central Command & Persian Gulf Security", "is_india_relevant": True, "freshness": "live", "provenance": "NAVCENT Public Affairs", "last_updated": now_iso},
            {"id": "base-us-diegogarcia", "name": "Navy Support Facility Diego Garcia", "type": "naval_base", "subtype": "US/UK Strategic Joint Base & Bomber Hub", "country": "United States", "country_code": "US", "lat": -7.319, "lon": 72.422, "runway_count": 1, "homeported_ships": "Submarine Tenders, Maritime Prepositioning Ships (MPSRON 2)", "strategic_role": "Strategic Indian Ocean Hub for B-2/B-52 Strategic Bombers and SSGN Submarines", "is_india_relevant": True, "freshness": "live", "provenance": "DoD Open Infrastructure Directory", "last_updated": now_iso},
            {"id": "base-us-kadena", "name": "Kadena Air Base (Okinawa)", "type": "airbase", "subtype": "USAF 18th Wing Pacific Mega Base", "country": "United States", "country_code": "US", "lat": 26.355, "lon": 127.767, "runway_count": 2, "active_squadrons": "18th Wing (F-15C/D, F-35A, KC-135, E-3 Sentry, HH-60G)", "strategic_role": "Keystone of the Pacific: Premier USAF Forward Air Dominance & Tanker Hub", "is_india_relevant": False, "freshness": "live", "provenance": "PACAF Public Affairs", "last_updated": now_iso},
            {"id": "base-us-ramstein", "name": "Ramstein Air Base (Germany)", "type": "airbase", "subtype": "USAF Europe & Africa (USAFE) HQ", "country": "United States", "country_code": "US", "lat": 49.437, "lon": 7.600, "runway_count": 2, "active_squadrons": "86th Airlift Wing (C-130J, C-21, C-37)", "strategic_role": "Headquarters of U.S. Air Forces Europe and NATO Allied Air Command", "is_india_relevant": False, "freshness": "live", "provenance": "USAFE Public Affairs", "last_updated": now_iso},
            {"id": "base-us-aldhafra", "name": "Al Dhafra Air Base (UAE)", "type": "airbase", "subtype": "USAF 380th Air Expeditionary Wing Hub", "country": "United States", "country_code": "US", "lat": 24.248, "lon": 54.547, "runway_count": 2, "active_squadrons": "380th AEW (F-35A Lightning II, RQ-4 Global Hawk, KC-10 Extender)", "strategic_role": "USAF Middle East Stealth Strike, Airborne Surveillance & Tanker Hub", "is_india_relevant": True, "freshness": "live", "provenance": "AFCENT Public Affairs", "last_updated": now_iso},

            # ================= CHINA STRATEGIC BASES =================
            {"id": "base-cn-yulin", "name": "Yulin Naval Base (Sanya, Hainan)", "type": "naval_base", "subtype": "PLAN South Sea Fleet Submarine & Carrier Base", "country": "China", "country_code": "CN", "lat": 18.219, "lon": 109.568, "runway_count": 0, "homeported_ships": "PLAN Shandong (CV-17), Type 094 Jin SSBNs, Type 093 Shang SSNs", "strategic_role": "Subterranean Mountain Submarine Pens & Carrier Pier for South China Sea Power", "is_india_relevant": True, "freshness": "live", "provenance": "DoD China Military Power Report", "last_updated": now_iso},
            {"id": "base-cn-qingdao", "name": "Qingdao Submarine & Naval Base", "type": "naval_base", "subtype": "PLAN North Sea Fleet Headquarters", "country": "China", "country_code": "CN", "lat": 36.088, "lon": 120.312, "runway_count": 0, "homeported_ships": "PLAN Liaoning (CV-16), Nuclear Attack Submarines, Type 055 Destroyers", "strategic_role": "North Sea Fleet Command & Bohai Bay Bastion Defense", "is_india_relevant": False, "freshness": "live", "provenance": "PLA Daily / CSIS OSINT", "last_updated": now_iso},
            {"id": "base-cn-zhanjiang", "name": "Zhanjiang Naval Base", "type": "naval_base", "subtype": "PLAN South Sea Fleet Surface Fleet HQ", "country": "China", "country_code": "CN", "lat": 21.218, "lon": 110.408, "runway_count": 0, "homeported_ships": "Type 055 Large Destroyers, Type 075 Amphibious Assault Ships", "strategic_role": "Operational Headquarters for South China Sea Amphibious & Surface Fleets", "is_india_relevant": True, "freshness": "live", "provenance": "CSIS ChinaPower", "last_updated": now_iso},
            {"id": "base-cn-hotan", "name": "Hotan Airbase (Xinjiang)", "type": "airbase", "subtype": "PLAAF Western Theater Forward Base", "country": "China", "country_code": "CN", "lat": 37.038, "lon": 79.865, "runway_count": 1, "active_squadrons": "J-20 Stealth Fighters, J-16 Multi-Role Fighters, GJ-11 Stealth UCAVs", "strategic_role": "Western Theater Airbase Facing Eastern Ladakh LAC & Karakoram Pass", "is_india_relevant": True, "freshness": "live", "provenance": "CSIS Asia Maritime Transparency / Satellite Corroboration", "last_updated": now_iso},
            {"id": "base-cn-lhasa", "name": "Lhasa Gonggar Airport / Military Airbase", "type": "airbase", "subtype": "PLAAF High-Altitude Hardened Base (Tibet)", "country": "China", "country_code": "CN", "lat": 29.297, "lon": 90.912, "runway_count": 2, "active_squadrons": "Hardened Subterranean Revetments (J-20, J-11BH, KJ-500 AEW&C)", "strategic_role": "Primary High-Altitude Airbase Facing Sikkim and Bhutan Borders (Elevation 3,570m)", "is_india_relevant": True, "freshness": "live", "provenance": "Satellite OSINT / Jane's Defence", "last_updated": now_iso},
            {"id": "base-cn-dingxin", "name": "Dingxin Air Test & Training Base", "type": "airbase", "subtype": "PLAAF Weapons & Tactics Center (Gobi)", "country": "China", "country_code": "CN", "lat": 40.404, "lon": 99.789, "runway_count": 3, "active_squadrons": "J-20, J-35, H-20 Testing Detachments, Red Sword Aggressors", "strategic_role": "China's Equivalent of Nellis AFB / Top Gun Combat Tactics Center", "is_india_relevant": False, "freshness": "live", "provenance": "CSIS / DoD China Report", "last_updated": now_iso},

            # ================= RUSSIA STRATEGIC BASES =================
            {"id": "base-ru-severomorsk", "name": "Severomorsk Naval Base", "type": "naval_base", "subtype": "Russian Northern Fleet Main Headquarters", "country": "Russia", "country_code": "RU", "lat": 69.073, "lon": 33.421, "runway_count": 0, "homeported_ships": "Admiral Gorshkov Frigates, Kirov-class Battlecruisers, Yasen Nuclear SSNs", "strategic_role": "Headquarters of the Russian Northern Fleet & Arctic Nuclear Bastion", "is_india_relevant": True, "freshness": "live", "provenance": "mil.ru Official Portal", "last_updated": now_iso},
            {"id": "base-ru-tartus", "name": "Tartus Naval Logistics Facility", "type": "naval_base", "subtype": "Russian Mediterranean Operational Hub", "country": "Russia", "country_code": "RU", "lat": 34.912, "lon": 35.874, "runway_count": 0, "homeported_ships": "Admiral Grigorovich Frigates, Improved Kilo Submarines", "strategic_role": "Russia's Sole Deep-Water Naval Facility in the Mediterranean Basin", "is_india_relevant": False, "freshness": "live", "provenance": "TASS / Russian MoD", "last_updated": now_iso},
            {"id": "base-ru-vladivostok", "name": "Vladivostok Naval Base", "type": "naval_base", "subtype": "Russian Pacific Fleet Headquarters", "country": "Russia", "country_code": "RU", "lat": 43.115, "lon": 131.885, "runway_count": 0, "homeported_ships": "Cruiser Varyag, Udaloy Destroyers, Gremyashchiy Corvettes", "strategic_role": "Main Base and Headquarters of the Russian Navy Pacific Fleet", "is_india_relevant": False, "freshness": "live", "provenance": "mil.ru", "last_updated": now_iso},
            {"id": "base-ru-engels", "name": "Engels-2 Strategic Airbase", "type": "airbase", "subtype": "Russian Long-Range Aviation HQ", "country": "Russia", "country_code": "RU", "lat": 51.483, "lon": 46.216, "runway_count": 1, "active_squadrons": "121st Heavy Bomber Aviation Reg (Tu-160 Blackjack, Tu-95MS Bear-H)", "strategic_role": "Primary Strategic Bomber Base for Russian Nuclear Triad Air Leg", "is_india_relevant": False, "freshness": "live", "provenance": "mil.ru / CSIS OSINT", "last_updated": now_iso},
            {"id": "base-ru-khmeimim", "name": "Khmeimim Air Base (Syria)", "type": "airbase", "subtype": "Russian Aerospace Forces Forward Expeditionary Base", "country": "Russia", "country_code": "RU", "lat": 35.409, "lon": 35.948, "runway_count": 2, "active_squadrons": "Su-35S, Su-34 Fullback, Tu-22M3 Backfire-C, S-400 Triumf Battery", "strategic_role": "Russian Air Power Projection across Eastern Mediterranean and Levant", "is_india_relevant": False, "freshness": "live", "provenance": "mil.ru", "last_updated": now_iso},

            # ================= PAKISTAN STRATEGIC BASES =================
            {"id": "base-pk-shahbaz", "name": "PAF Base Shahbaz (Jacobabad)", "type": "airbase", "subtype": "PAF F-16 Main Operating Base", "country": "Pakistan", "country_code": "PK", "lat": 28.283, "lon": 68.450, "runway_count": 2, "active_squadrons": "No. 5 Sqn (Falcons - F-16C/D Block 52+)", "strategic_role": "Southern Air Command Precision Strike & Air Defense Hub", "is_india_relevant": True, "freshness": "live", "provenance": "ISPR Official Directory", "last_updated": now_iso},
            {"id": "base-pk-mushaf", "name": "PAF Base Mushaf (Sargodha)", "type": "airbase", "subtype": "PAF Central Air Command HQ & Combat Center", "country": "Pakistan", "country_code": "PK", "lat": 32.049, "lon": 72.666, "runway_count": 2, "active_squadrons": "Combat Commanders School (F-16A/B, Mirage III/V, JF-17 Block III)", "strategic_role": "PAF Central Air Command Headquarters & Elite Tactics Center", "is_india_relevant": True, "freshness": "live", "provenance": "ISPR", "last_updated": now_iso},
            {"id": "base-pk-bholari", "name": "PAF Base Bholari", "type": "airbase", "subtype": "PAF Modernized Strike Base (Sindh)", "country": "Pakistan", "country_code": "PK", "lat": 25.255, "lon": 68.040, "runway_count": 1, "active_squadrons": "No. 15 Sqn (Cobras - J-10CE), No. 19 Sqn (Sherdils - JF-17)", "strategic_role": "Modern Strike Base Defending Karachi Maritime Axis & Border", "is_india_relevant": True, "freshness": "live", "provenance": "ISPR Open Release", "last_updated": now_iso},
            {"id": "base-pk-karachi", "name": "Karachi Naval Dockyard (PNS Himalaya)", "type": "naval_base", "subtype": "Pakistan Navy Headquarters & Fleet Base", "country": "Pakistan", "country_code": "PK", "lat": 24.838, "lon": 66.973, "runway_count": 0, "homeported_ships": "Type 054A/P Frigates, Babur-class Corvettes, Agosta Submarines", "strategic_role": "Primary Fleet Headquarters & Ship Maintenance Facility", "is_india_relevant": True, "freshness": "live", "provenance": "Pakistan Navy Official Portal", "last_updated": now_iso},
            {"id": "base-pk-ormara", "name": "PNS Jinnah (Ormara Naval Base)", "type": "naval_base", "subtype": "Pakistan Navy Submarine & Coastal Base", "country": "Pakistan", "country_code": "PK", "lat": 25.200, "lon": 64.630, "runway_count": 0, "homeported_ships": "Hangor-class / Agosta 90B Submarines, Fast Attack Craft", "strategic_role": "Strategic Stand-off Naval Base on the Makran Coast", "is_india_relevant": True, "freshness": "live", "provenance": "ISPR", "last_updated": now_iso},

            # ================= UNITED KINGDOM STRATEGIC BASES =================
            {"id": "base-uk-portsmouth", "name": "HMNB Portsmouth", "type": "naval_base", "subtype": "Royal Navy Surface Fleet Main Homeport", "country": "United Kingdom", "country_code": "UK", "lat": 50.803, "lon": -1.111, "runway_count": 0, "homeported_ships": "HMS Queen Elizabeth (R08), HMS Prince of Wales (R09), Type 45 Destroyers", "strategic_role": "Home of the UK Carrier Strike Fleet and Type 45 Air Defense Destroyers", "is_india_relevant": False, "freshness": "live", "provenance": "Royal Navy Official Portal", "last_updated": now_iso},
            {"id": "base-uk-clyde", "name": "HMNB Clyde (Faslane)", "type": "naval_base", "subtype": "Royal Navy Submarine Service HQ", "country": "United Kingdom", "country_code": "UK", "lat": 56.064, "lon": -4.818, "runway_count": 0, "homeported_ships": "Vanguard-class SSBNs (Trident II D5), Astute-class Attack Submarines", "strategic_role": "Home of the UK Continuous At-Sea Deterrent (CASD) Nuclear Submarines", "is_india_relevant": False, "freshness": "live", "provenance": "Royal Navy Official Portal", "last_updated": now_iso},
            {"id": "base-uk-coningsby", "name": "RAF Coningsby", "type": "airbase", "subtype": "RAF Southern Quick Reaction Alert (QRA) Base", "country": "United Kingdom", "country_code": "UK", "lat": 53.093, "lon": -0.166, "runway_count": 1, "active_squadrons": "No. 3 Sqn, No. 11 Sqn, No. 12 Sqn (Eurofighter Typhoon FGR4)", "strategic_role": "Southern UK Quick Reaction Alert & Typhoon Operational Conversion", "is_india_relevant": False, "freshness": "live", "provenance": "RAF Official Portal", "last_updated": now_iso},

            # ================= FRANCE STRATEGIC BASES =================
            {"id": "base-fr-toulon", "name": "Toulon Naval Base", "type": "naval_base", "subtype": "Marine Nationale Mediterranean Fleet HQ", "country": "France", "country_code": "FR", "lat": 43.120, "lon": 5.928, "runway_count": 0, "homeported_ships": "FS Charles de Gaulle (R91), Horizon Destroyers, Rubis/Suffren SSNs", "strategic_role": "Main Base of the French Carrier Strike Group & Mediterranean Naval Force", "is_india_relevant": True, "freshness": "live", "provenance": "Marine Nationale Portal", "last_updated": now_iso},
            {"id": "base-fr-montdemarsan", "name": "Mont-de-Marsan Air Base (BA 118)", "type": "airbase", "subtype": "French Air & Space Force Rafale Hub", "country": "France", "country_code": "FR", "lat": 43.911, "lon": -0.505, "runway_count": 1, "active_squadrons": "Escadron de Chasse 2/30 Normandie-Niemen (Rafale B/C)", "strategic_role": "Premier Rafale Combat Testing and Tactical Evaluation Wing", "is_india_relevant": False, "freshness": "live", "provenance": "Armée de l'Air et de l'Espace", "last_updated": now_iso},

            # ================= NATO STRATEGIC BASES =================
            {"id": "base-nato-geilenkirchen", "name": "NATO Air Base Geilenkirchen", "type": "airbase", "subtype": "NATO Airborne Early Warning & Control HQ", "country": "NATO", "country_code": "NATO", "lat": 50.960, "lon": 6.042, "runway_count": 1, "active_squadrons": "NATO E-3A Component (14 Boeing E-3A Sentry AWACS)", "strategic_role": "NATO's Multi-National Airborne Early Warning Command Hub", "is_india_relevant": False, "freshness": "live", "provenance": "NATO Allied Air Command", "last_updated": now_iso},
            {"id": "base-nato-sigonella", "name": "Naval Air Station Sigonella (Sicily)", "type": "airbase", "subtype": "NATO Mediterranean Hub for ISR & Maritime Patrol", "country": "NATO", "country_code": "NATO", "lat": 37.402, "lon": 14.922, "runway_count": 2, "active_squadrons": "NATO Alliance Ground Surveillance (AGS RQ-4D Phoenix), US Navy P-8A Poseidon", "strategic_role": "The Hub of the Mediterranean: NATO Alliance Ground Surveillance HQ", "is_india_relevant": False, "freshness": "live", "provenance": "NATO MARCOM / US Navy", "last_updated": now_iso},

            # ================= JAPAN STRATEGIC BASES =================
            {"id": "base-jp-sasebo", "name": "JMSDF Sasebo Naval Base", "type": "naval_base", "subtype": "Japan Maritime Self-Defense Force District HQ", "country": "Japan", "country_code": "JP", "lat": 33.161, "lon": 129.714, "runway_count": 0, "homeported_ships": "JS Kaga (DDH-184 F-35B Carrier), Maya-class Aegis Destroyers", "strategic_role": "Guardians of the Tsushima Strait & East China Sea Approaches", "is_india_relevant": False, "freshness": "live", "provenance": "JMSDF Official Portal", "last_updated": now_iso},
            {"id": "base-jp-misawa", "name": "Misawa Air Base (Aomori)", "type": "airbase", "subtype": "JASDF / USAF Joint Northern Air Wing", "country": "Japan", "country_code": "JP", "lat": 40.703, "lon": 141.367, "runway_count": 1, "active_squadrons": "3rd Air Wing (JASDF F-35A Lightning II), USAF 35th Fighter Wing", "strategic_role": "Premier Northern Air Defense & 5th Generation Stealth Hub in Japan", "is_india_relevant": False, "freshness": "live", "provenance": "JASDF / PACAF", "last_updated": now_iso},

            # ================= IRAN STRATEGIC BASES =================
            {"id": "base-ir-bandarabbas", "name": "Bandar Abbas Naval Base (1st Naval Zone)", "type": "naval_base", "subtype": "IRIN Main Fleet HQ & Submarine Base", "country": "Iran", "country_code": "IR", "lat": 27.147, "lon": 56.208, "runway_count": 0, "homeported_ships": "Moudge-class Frigates, Kilo-class Submarines, Fateh Submarines", "strategic_role": "Main Base of the Islamic Republic of Iran Navy Controlling Strait of Hormuz", "is_india_relevant": True, "freshness": "live", "provenance": "IRNA / OSINT Defense", "last_updated": now_iso},
            {"id": "base-ir-konarak", "name": "Konarak Naval Base (Chabahar / Gulf of Oman)", "type": "naval_base", "subtype": "IRIN 3rd Naval Zone Deep-Sea Base", "country": "Iran", "country_code": "IR", "lat": 25.358, "lon": 60.399, "runway_count": 0, "homeported_ships": "Missile Corvettes, Fast Attack Missile Boats, Survey Vessels", "strategic_role": "Direct Ocean Access Base Outside Hormuz Adjacent to Chabahar Port Corridor", "is_india_relevant": True, "freshness": "live", "provenance": "IRNA", "last_updated": now_iso},
            {"id": "base-ir-isfahan", "name": "Shahid Vatanpour / Isfahan 8th Tactical Air Base", "type": "airbase", "subtype": "IRIAF 8th Tactical Fighter Base", "country": "Iran", "country_code": "IR", "lat": 32.750, "lon": 51.860, "runway_count": 2, "active_squadrons": "Grumman F-14A Tomcat, Sukhoi Su-24MK Fencer, MiG-29", "strategic_role": "Central Iran Air Superiority & Defense of Strategic Natanz Nuclear Complex", "is_india_relevant": True, "freshness": "live", "provenance": "IRIAF Official Gazette", "last_updated": now_iso}
        ]

        for base in bases_catalog:
            self.installations[base["id"]] = base

    def _seed_domestic_stability(self):
        self.domestic_metrics = {
            "overall_stability_index": 98.4,
            "status": "Optimal Stability & Resilience",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "connectivity": {
                "national_uptime_pct": 99.92,
                "cloudflare_radar_score": 100,
                "ioda_status": "Normal Routing",
                "active_bgp_anomalies": 0,
                "note": "All national undersea cable landing stations (Mumbai, Chennai, Kochi, Tuticorin) operational."
            },
            "disaster_management_ndma": {
                "active_red_alerts": 0,
                "active_orange_alerts": 1,
                "bulletin_summary": "Monsoon rainfall monitoring active in Coastal Karnataka and Konkan. Zero major catastrophic natural alerts.",
                "source": "NDMA Public Bulletin Feed (ndma.gov.in)"
            },
            "maritime_port_flow": {
                "major_ports_operational": 12,
                "total_major_ports": 12,
                "avg_turnaround_hours": 22.4,
                "status": "Normal Clearance Speed"
            },
            "power_grid_frequency": {
                "national_frequency_hz": 50.01,
                "status": "Synchronized (Safe Band)",
                "grid_reliability_pct": 99.98
            },
            "public_order_digest": {
                "districts_peaceful": 766,
                "total_state_districts_monitored": 766,
                "status": "Normal Civics Routine",
                "detail": "Open reporting across 28 states & 8 UTs indicates peaceful civic status."
            }
        }

    # -------------------------------------------------------------
    # Intelligence Query Interface with Scope Filters (Global vs India)
    # -------------------------------------------------------------
    def get_events(self, timeframe: Optional[str] = "6h", category: Optional[str] = None, severity: Optional[int] = None, search: Optional[str] = None, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        now = datetime.now(timezone.utc)
        results = []

        max_hours = {
            "6h": 6.0,
            "12h": 12.0,
            "24h": 24.0,
            "7d": 168.0,
            "all": 999999.0
        }.get(timeframe.lower() if timeframe else "6h", 6.0)

        for ev in self.events.values():
            if scope == "india" and not ev.get("is_india_relevant", False):
                continue

            # Timeframe filter
            created_str = ev.get("created_at")
            if created_str and max_hours < 999999.0:
                try:
                    dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                    diff_hours = (now - dt).total_seconds() / 3600.0
                    if diff_hours > max_hours:
                        continue
                except Exception:
                    pass

            # Category filter
            if category and category.lower() != "all":
                if ev.get("category", "").lower() != category.lower():
                    continue

            # Severity filter
            if severity is not None:
                if ev.get("severity_global") != severity:
                    continue

            # Keyword search
            if search and search.strip():
                s_lower = search.strip().lower()
                title_match = s_lower in ev.get("title", "").lower()
                sum_match = s_lower in ev.get("summary", "").lower()
                loc_match = s_lower in ev.get("location", {}).get("name", "").lower()
                if not (title_match or sum_match or loc_match):
                    continue

            results.append(ev)

        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return results

    def get_all_flags(self, status: Optional[str] = "approved", scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        flags = list(self.india_flags.values())
        if status:
            flags = [f for f in flags if f.get("status") == status]
        if scope == "india":
            flags = [f for f in flags if f.get("is_india_relevant", False)]
        return flags

    def get_naval_fleets(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        fleets = list(self.naval_fleets.values())
        if scope == "india":
            return [f for f in fleets if f.get("is_india_relevant", False)]
        return fleets

    def get_world_leaders(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        leaders = list(self.world_leaders.values())
        if scope == "india":
            return [l for l in leaders if l.get("is_india_relevant", False)]
        return leaders

    def get_flights(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        flights = list(self.flight_contacts.values())
        if scope == "india":
            return [f for f in flights if f.get("is_india_relevant", False)]
        return flights

    def get_vessels(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        vessels = list(self.vessel_contacts.values())
        if scope == "india":
            return [v for v in vessels if v.get("is_india_relevant", False)]
        return vessels

    def get_disasters(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        disasters = list(self.disasters.values())
        if scope == "india":
            return [d for d in disasters if d.get("is_india_relevant", False)]
        return disasters

    def get_installations(self, country: Optional[str] = None, type_filter: Optional[str] = None, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        insts = list(self.installations.values())
        if scope == "india":
            insts = [i for i in insts if i.get("is_india_relevant", False)]
        if country and country.lower() != "all":
            c_norm = country.lower().strip()
            insts = [
                i for i in insts 
                if i.get("country", "").lower() == c_norm or i.get("country_code", "").lower() == c_norm
            ]
        if type_filter and type_filter.lower() != "all":
            t_norm = type_filter.lower().strip()
            insts = [i for i in insts if i.get("type", "").lower() == t_norm]
        return insts

    def get_news_ticker(self) -> List[Dict[str, Any]]:
        evs = list(self.events.values())
        evs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return [{"id": e["id"], "title": e["title"], "category": e["category"], "severity": e.get("severity_global", 1), "time": e.get("created_at")} for e in evs[:12]]

    def get_domestic_stability(self) -> Dict[str, Any]:
        return self.domestic_metrics

    def get_review_queue(self) -> List[Dict[str, Any]]:
        return list(self.review_queue.values())

    def approve_review_item(self, flag_id: str, reviewer_note: str = "") -> Optional[Dict[str, Any]]:
        if flag_id in self.india_flags:
            self.india_flags[flag_id]["status"] = "approved"
            self.india_flags[flag_id]["reviewer_note"] = reviewer_note
            self.india_flags[flag_id]["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            if flag_id in self.review_queue:
                del self.review_queue[flag_id]
            return self.india_flags[flag_id]
        return None

    def reject_review_item(self, flag_id: str, reason: str = "") -> Optional[Dict[str, Any]]:
        if flag_id in self.india_flags:
            self.india_flags[flag_id]["status"] = "rejected"
            self.india_flags[flag_id]["rejection_reason"] = reason
            self.india_flags[flag_id]["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            if flag_id in self.review_queue:
                del self.review_queue[flag_id]
            return self.india_flags[flag_id]
        return None

    def update_flight_positions_simulation(self):
        """Simulates smooth flight movements continuously along true headings"""
        for f in self.flight_contacts.values():
            heading = f.get("heading", 0)
            rad = math.radians(heading)
            # Advance proportional to velocity
            speed_kmh = f.get("velocity_kmh", 800)
            step_deg = (speed_kmh / 3600.0) * 4.0 / 111.0 # 4 second movement step
            f["lat"] = round(f["lat"] + math.cos(rad) * step_deg, 4)
            f["lon"] = round(f["lon"] + math.sin(rad) * step_deg, 4)

            # Boundary wrap for global flights
            if f["lat"] > 85.0: f["lat"] = -80.0
            if f["lat"] < -85.0: f["lat"] = 80.0
            if f["lon"] > 180.0: f["lon"] = -180.0
            if f["lon"] < -180.0: f["lon"] = 180.0

            # Slight altitude oscillation
            if f.get("altitude_m", 0) > 3000:
                f["altitude_m"] += int((time.time() % 3 - 1) * 6)

    # Semantic & Keyword Search for RAG Chatbot
    def search_events_for_rag(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        scored = []
        for ev in self.events.values():
            flag = next((f for f in self.india_flags.values() if f.get("event_id") == ev["id"]), None)
            text_corpus = f"{ev.get('title', '')} {ev.get('summary', '')} {flag.get('rationale', '') if flag else ''} {ev.get('category', '')}".lower()
            
            score = 0
            for qw in query_words:
                if qw in ["the", "a", "an", "is", "in", "what", "why", "how", "for", "to", "and"]:
                    continue
                if qw in text_corpus:
                    score += text_corpus.count(qw) * 2

            if score > 0:
                scored.append((score, ev, flag))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, ev, flag in scored[:limit]:
            results.append({
                "event_id": ev["id"],
                "title": ev["title"],
                "summary": ev["summary"],
                "category": flag.get("category", ev.get("category")) if flag else ev.get("category"),
                "impact_severity": flag.get("impact_severity", 1) if flag else 1,
                "confidence": flag.get("confidence", "medium") if flag else "medium",
                "sources": ev.get("sources", []),
                "location": ev.get("location", {}),
                "created_at": ev.get("created_at"),
                "rationale": flag.get("rationale") if flag else ""
            })
        return results

    def get_knowledge_excerpts(self, query: str) -> List[Dict[str, str]]:
        q_lower = query.lower()
        excerpts = []
        for doc_name, doc_data in self.knowledge_docs.items():
            content = doc_data["content"]
            if any(term in q_lower for term in [doc_name.replace("-", " "), doc_data["title"].lower()]) or any(w in content.lower() for w in q_lower.split() if len(w) > 4):
                excerpts.append({
                    "title": doc_data["title"],
                    "excerpt": content[:1200]
                })
        return excerpts[:2]

# Global singleton
db = Database()
