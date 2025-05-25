#!/usr/bin/env python3
"""
Instagram Intelligence Analyzer - เครื่องมือวิเคราะห์ข้อมูลขาดใจ
สำหรับการวิเคราะห์ข้อมูลที่สกัดมาจาก Instagram เพื่อสร้าง behavioral profile

🎯 Target: alx.trading
📊 Analysis: Behavioral patterns, social networks, content preferences
🧠 Intelligence: Psychological profiling, targeting vectors
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter
import re
from typing import Dict, List, Any

class InstagramIntelligenceAnalyzer:
    def __init__(self, extraction_file=None):
        """Initialize intelligence analyzer"""
        self.extraction_file = extraction_file
        self.intelligence_data = {
            "timestamp": datetime.now().isoformat(),
            "target": "alx.trading",
            "analysis_version": "advanced_v2.0",
            "behavioral_profile": {},
            "social_network_analysis": {},
            "content_analysis": {},
            "communication_patterns": {},
            "psychological_profile": {},
            "targeting_vectors": {},
            "risk_assessment": {},
            "intelligence_summary": {}
        }
        
        self.raw_data = {}
        if extraction_file and os.path.exists(extraction_file):
            self.load_extraction_data(extraction_file)
    
    def load_extraction_data(self, filename):
        """Load extracted Instagram data for analysis"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.raw_data = json.load(f)
            print(f"✅ Loaded extraction data from {filename}")
        except Exception as e:
            print(f"❌ Failed to load data: {str(e)}")
    
    def analyze_behavioral_patterns(self):
        """Analyze behavioral patterns from all data sources"""
        print("🧠 Analyzing behavioral patterns...")
        
        if not self.raw_data.get('data'):
            return
        
        data = self.raw_data['data']
        patterns = {
            "activity_times": [],
            "posting_frequency": {},
            "engagement_patterns": {},
            "content_preferences": {},
            "social_behavior": {},
            "communication_style": {}
        }
        
        # Analyze posting patterns
        if data.get('posts'):
            post_times = []
            for post in data['posts']:
                try:
                    timestamp = datetime.fromisoformat(post['timestamp'].replace('Z', '+00:00'))
                    post_times.append({
                        "hour": timestamp.hour,
                        "day_of_week": timestamp.weekday(),
                        "engagement_rate": post.get('engagement_rate', 0)
                    })
                except:
                    continue
            
            if post_times:
                # Most active hours
                hours = [p['hour'] for p in post_times]
                hour_counter = Counter(hours)
                patterns["activity_times"] = {
                    "most_active_hours": hour_counter.most_common(3),
                    "avg_posting_hour": sum(hours) / len(hours),
                    "posting_schedule": "consistent" if len(set(hours)) <= 8 else "irregular"
                }
                
                # Engagement patterns
                avg_engagement = sum(p['engagement_rate'] for p in post_times) / len(post_times)
                patterns["engagement_patterns"] = {
                    "average_engagement_rate": round(avg_engagement, 2),
                    "peak_engagement_hours": [h for p in post_times for h in [p['hour']] if p['engagement_rate'] > avg_engagement],
                    "engagement_consistency": "high" if max(p['engagement_rate'] for p in post_times) - min(p['engagement_rate'] for p in post_times) < 5 else "variable"
                }
        
        # Analyze content preferences
        if data.get('posts'):
            content_analysis = {
                "media_preference": {},
                "hashtag_patterns": [],
                "location_usage": [],
                "caption_style": {}
            }
            
            video_count = sum(1 for post in data['posts'] if post.get('is_video'))
            photo_count = len(data['posts']) - video_count
            
            content_analysis["media_preference"] = {
                "prefers_videos": video_count > photo_count,
                "video_percentage": round(video_count / max(len(data['posts']), 1) * 100, 1),
                "content_type": "video-focused" if video_count > photo_count else "photo-focused"
            }
            
            # Hashtag analysis
            all_hashtags = []
            caption_lengths = []
            location_count = 0
            
            for post in data['posts']:
                hashtags = post.get('hashtags', [])
                all_hashtags.extend(hashtags)
                
                caption = post.get('caption', '')
                caption_lengths.append(len(caption))
                
                if post.get('location'):
                    location_count += 1
            
            if all_hashtags:
                hashtag_counter = Counter(all_hashtags)
                content_analysis["hashtag_patterns"] = {
                    "most_used_hashtags": hashtag_counter.most_common(10),
                    "avg_hashtags_per_post": round(len(all_hashtags) / max(len(data['posts']), 1), 1),
                    "hashtag_categories": self.categorize_hashtags(all_hashtags)
                }
            
            if caption_lengths:
                avg_caption_length = sum(caption_lengths) / len(caption_lengths)
                content_analysis["caption_style"] = {
                    "average_caption_length": round(avg_caption_length, 0),
                    "writing_style": "detailed" if avg_caption_length > 200 else "concise" if avg_caption_length > 50 else "minimal",
                    "uses_locations": round(location_count / max(len(data['posts']), 1) * 100, 1)
                }
            
            patterns["content_preferences"] = content_analysis
        
        # Analyze social behavior from DMs
        if data.get('direct_messages'):
            social_patterns = {
                "communication_frequency": {},
                "response_patterns": {},
                "conversation_types": {}
            }
            
            active_conversations = sum(1 for dm in data['direct_messages'] if dm.get('analysis', {}).get('conversation_active', False))
            total_conversations = len(data['direct_messages'])
            
            social_patterns["communication_frequency"] = {
                "total_dm_threads": total_conversations,
                "active_conversations": active_conversations,
                "social_activity_level": "high" if active_conversations > 5 else "medium" if active_conversations > 2 else "low"
            }
            
            patterns["social_behavior"] = social_patterns
        
        self.intelligence_data["behavioral_profile"] = patterns
    
    def categorize_hashtags(self, hashtags):
        """Categorize hashtags by topic"""
        categories = {
            "lifestyle": ["#lifestyle", "#life", "#daily", "#mood", "#vibes"],
            "business": ["#business", "#entrepreneur", "#trading", "#finance", "#money"],
            "travel": ["#travel", "#trip", "#vacation", "#explore", "#adventure"],
            "fitness": ["#fitness", "#gym", "#workout", "#health", "#sport"],
            "food": ["#food", "#restaurant", "#cooking", "#delicious", "#yummy"],
            "fashion": ["#fashion", "#style", "#outfit", "#clothes", "#shopping"],
            "personal": ["#me", "#selfie", "#myself", "#personal", "#thoughts"]
        }
        
        hashtag_categories = {}
        for category, keywords in categories.items():
            matches = sum(1 for hashtag in hashtags if any(keyword in hashtag.lower() for keyword in keywords))
            if matches > 0:
                hashtag_categories[category] = matches
        
        return hashtag_categories
    
    def analyze_social_network(self):
        """Analyze social network connections and influence"""
        print("👥 Analyzing social network...")
        
        if not self.raw_data.get('data'):
            return
        
        data = self.raw_data['data']
        network_analysis = {
            "follower_analysis": {},
            "following_analysis": {},
            "influence_metrics": {},
            "network_quality": {}
        }
        
        account_info = data.get('account_info', {})
        followers_sample = data.get('followers_sample', [])
        following_sample = data.get('following_sample', [])
        
        # Follower analysis
        if account_info:
            follower_count = account_info.get('followers_count', 0)
            following_count = account_info.get('following_count', 0)
            
            network_analysis["influence_metrics"] = {
                "follower_count": follower_count,
                "following_count": following_count,
                "follow_ratio": round(follower_count / max(following_count, 1), 2),
                "influence_level": "high" if follower_count > 10000 else "medium" if follower_count > 1000 else "low",
                "account_selectivity": "selective" if following_count < follower_count * 0.5 else "social"
            }
        
        # Analyze follower quality
        if followers_sample:
            verified_followers = sum(1 for f in followers_sample if f.get('is_verified'))
            private_followers = sum(1 for f in followers_sample if f.get('is_private'))
            
            avg_follower_count = sum(f.get('follower_count', 0) for f in followers_sample) / len(followers_sample)
            
            network_analysis["follower_analysis"] = {
                "sample_size": len(followers_sample),
                "verified_percentage": round(verified_followers / len(followers_sample) * 100, 1),
                "private_percentage": round(private_followers / len(followers_sample) * 100, 1),
                "avg_follower_influence": round(avg_follower_count, 0),
                "follower_quality": "high" if verified_followers > 0 or avg_follower_count > 1000 else "medium"
            }
        
        # Analyze following patterns
        if following_sample:
            verified_following = sum(1 for f in following_sample if f.get('is_verified'))
            business_accounts = sum(1 for f in following_sample if f.get('follower_count', 0) > 10000)
            
            network_analysis["following_analysis"] = {
                "sample_size": len(following_sample),
                "follows_verified_accounts": verified_following,
                "follows_influencers": business_accounts,
                "following_strategy": "quality-focused" if verified_following > len(following_sample) * 0.1 else "broad-reach"
            }
        
        self.intelligence_data["social_network_analysis"] = network_analysis
    
    def analyze_communication_patterns(self):
        """Analyze communication patterns from DMs"""
        print("💬 Analyzing communication patterns...")
        
        if not self.raw_data.get('data', {}).get('direct_messages'):
            return
        
        dm_data = self.raw_data['data']['direct_messages']
        patterns = {
            "conversation_analysis": {},
            "response_behavior": {},
            "communication_style": {},
            "relationship_patterns": {}
        }
        
        total_threads = len(dm_data)
        active_threads = sum(1 for dm in dm_data if dm.get('analysis', {}).get('conversation_active', False))
        
        # Analyze message content and frequency
        total_messages = sum(dm.get('message_count', 0) for dm in dm_data)
        avg_messages_per_thread = total_messages / max(total_threads, 1)
        
        patterns["conversation_analysis"] = {
            "total_dm_threads": total_threads,
            "active_conversations": active_threads,
            "avg_messages_per_conversation": round(avg_messages_per_thread, 1),
            "communication_activity": "high" if active_threads > 10 else "medium" if active_threads > 5 else "low"
        }
        
        # Analyze conversation partners
        conversation_types = {}
        for dm in dm_data:
            users = dm.get('users', [])
            if len(users) == 1:  # Direct conversation
                user = users[0]
                is_verified = user.get('is_verified', False)
                conversation_types['verified'] = conversation_types.get('verified', 0) + (1 if is_verified else 0)
                conversation_types['regular'] = conversation_types.get('regular', 0) + (1 if not is_verified else 0)
            else:  # Group conversation
                conversation_types['group'] = conversation_types.get('group', 0) + 1
        
        patterns["relationship_patterns"] = {
            "conversation_types": conversation_types,
            "prefers_direct_messages": conversation_types.get('regular', 0) + conversation_types.get('verified', 0) > conversation_types.get('group', 0),
            "connects_with_verified": conversation_types.get('verified', 0) > 0
        }
        
        self.intelligence_data["communication_patterns"] = patterns
    
    def create_psychological_profile(self):
        """Create psychological profile based on all analysis"""
        print("🧠 Creating psychological profile...")
        
        profile = {
            "personality_traits": {},
            "behavioral_tendencies": {},
            "social_preferences": {},
            "vulnerability_assessment": {},
            "manipulation_vectors": {}
        }
        
        # Analyze personality from content and behavior
        behavioral_data = self.intelligence_data.get("behavioral_profile", {})
        social_data = self.intelligence_data.get("social_network_analysis", {})
        communication_data = self.intelligence_data.get("communication_patterns", {})
        
        # Personality traits inference
        traits = {}
        
        # Extraversion analysis
        follower_count = social_data.get("influence_metrics", {}).get("follower_count", 0)
        posting_frequency = len(self.raw_data.get('data', {}).get('posts', []))
        social_activity = communication_data.get("conversation_analysis", {}).get("communication_activity", "low")
        
        extraversion_score = 0
        if follower_count > 1000: extraversion_score += 2
        if posting_frequency > 20: extraversion_score += 2
        if social_activity == "high": extraversion_score += 2
        
        traits["extraversion"] = "high" if extraversion_score >= 4 else "medium" if extraversion_score >= 2 else "low"
        
        # Openness to experience
        content_prefs = behavioral_data.get("content_preferences", {})
        hashtag_categories = content_prefs.get("hashtag_patterns", {}).get("hashtag_categories", {})
        
        openness_score = len(hashtag_categories)  # Variety of interests
        if content_prefs.get("media_preference", {}).get("prefers_videos"): openness_score += 1
        
        traits["openness"] = "high" if openness_score >= 4 else "medium" if openness_score >= 2 else "low"
        
        # Conscientiousness
        posting_schedule = behavioral_data.get("activity_times", {}).get("posting_schedule", "irregular")
        caption_style = content_prefs.get("caption_style", {}).get("writing_style", "minimal")
        
        conscientiousness_score = 0
        if posting_schedule == "consistent": conscientiousness_score += 2
        if caption_style == "detailed": conscientiousness_score += 2
        
        traits["conscientiousness"] = "high" if conscientiousness_score >= 3 else "medium" if conscientiousness_score >= 1 else "low"
        
        profile["personality_traits"] = traits
        
        # Vulnerability assessment
        vulnerabilities = {}
        
        # Social validation needs
        avg_engagement = behavioral_data.get("engagement_patterns", {}).get("average_engagement_rate", 0)
        if avg_engagement > 5:
            vulnerabilities["validation_seeking"] = "high"
        elif avg_engagement > 2:
            vulnerabilities["validation_seeking"] = "medium"
        else:
            vulnerabilities["validation_seeking"] = "low"
        
        # Financial interests (from hashtags)
        business_hashtags = hashtag_categories.get("business", 0)
        if business_hashtags > 0:
            vulnerabilities["financial_motivation"] = "high"
            vulnerabilities["money_focused"] = True
        
        # Social influence susceptibility
        follows_verified = social_data.get("following_analysis", {}).get("follows_verified_accounts", 0)
        if follows_verified > 0:
            vulnerabilities["authority_influence"] = "high"
            vulnerabilities["status_conscious"] = True
        
        profile["vulnerability_assessment"] = vulnerabilities
        
        # Manipulation vectors based on profile
        vectors = {}
        
        if vulnerabilities.get("financial_motivation") == "high":
            vectors["financial_seduction"] = {
                "effectiveness": "high",
                "approach": "wealth_display_luxury_lifestyle",
                "methods": ["expensive_gifts", "investment_opportunities", "business_partnerships"]
            }
        
        if vulnerabilities.get("validation_seeking") == "high":
            vectors["ego_manipulation"] = {
                "effectiveness": "high",
                "approach": "admiration_and_praise",
                "methods": ["compliments_on_success", "recognition_of_achievements", "social_status_elevation"]
            }
        
        if traits["extraversion"] == "high":
            vectors["social_seduction"] = {
                "effectiveness": "medium",
                "approach": "social_circle_infiltration",
                "methods": ["exclusive_events", "networking_opportunities", "social_proof"]
            }
        
        profile["manipulation_vectors"] = vectors
        
        self.intelligence_data["psychological_profile"] = profile
    
    def generate_targeting_vectors(self):
        """Generate comprehensive targeting vectors for seduction operations"""
        print("🎯 Generating targeting vectors...")
        
        vectors = {
            "primary_vectors": {},
            "secondary_vectors": {},
            "approach_strategies": {},
            "timing_recommendations": {},
            "risk_mitigation": {}
        }
        
        psych_profile = self.intelligence_data.get("psychological_profile", {})
        behavioral_profile = self.intelligence_data.get("behavioral_profile", {})
        social_analysis = self.intelligence_data.get("social_network_analysis", {})
        
        # Primary vectors based on psychological vulnerabilities
        vulnerabilities = psych_profile.get("vulnerability_assessment", {})
        manipulation_vectors = psych_profile.get("manipulation_vectors", {})
        
        if "financial_seduction" in manipulation_vectors:
            vectors["primary_vectors"]["financial_dominance"] = {
                "probability": "95%",
                "approach": "Wealthy trader/investor persona",
                "tactics": [
                    "Display trading success and luxury lifestyle",
                    "Offer exclusive investment opportunities",
                    "Create financial dependency through gifts",
                    "Position as mentor and financial guide"
                ],
                "timeline": "2-4 weeks for initial attraction, 6-8 weeks for dependency"
            }
        
        if "ego_manipulation" in manipulation_vectors:
            vectors["primary_vectors"]["validation_seduction"] = {
                "probability": "90%",
                "approach": "Admirer and status elevator",
                "tactics": [
                    "Constant admiration of achievements",
                    "Social media engagement and praise",
                    "Introduction to higher status social circles",
                    "Recognition and celebration of successes"
                ],
                "timeline": "1-2 weeks for attention, 4-6 weeks for emotional dependency"
            }
        
        # Secondary vectors
        traits = psych_profile.get("personality_traits", {})
        
        if traits.get("extraversion") == "high":
            vectors["secondary_vectors"]["social_infiltration"] = {
                "probability": "75%",
                "approach": "Social circle expansion",
                "tactics": [
                    "Organize exclusive networking events",
                    "Introduce to influential contacts",
                    "Create social FOMO (fear of missing out)",
                    "Become indispensable social connector"
                ]
            }
        
        if traits.get("openness") == "high":
            vectors["secondary_vectors"]["experience_seduction"] = {
                "probability": "80%",
                "approach": "Adventure and new experiences",
                "tactics": [
                    "Exotic travel opportunities",
                    "Unique cultural experiences",
                    "Intellectual stimulation and learning",
                    "Access to exclusive events and locations"
                ]
            }
        
        # Timing recommendations based on activity patterns
        activity_times = behavioral_profile.get("activity_times", {})
        if activity_times:
            most_active_hours = activity_times.get("most_active_hours", [])
            if most_active_hours:
                optimal_hours = [hour for hour, count in most_active_hours]
                vectors["timing_recommendations"] = {
                    "optimal_contact_hours": optimal_hours,
                    "engagement_strategy": "Initiate contact during peak activity times",
                    "response_probability": "highest during" + str(optimal_hours)
                }
        
        # Risk mitigation
        influence_level = social_analysis.get("influence_metrics", {}).get("influence_level", "low")
        follower_count = social_analysis.get("influence_metrics", {}).get("follower_count", 0)
        
        vectors["risk_mitigation"] = {
            "public_exposure_risk": "high" if follower_count > 10000 else "medium" if follower_count > 1000 else "low",
            "social_verification_risk": "high" if social_analysis.get("follower_analysis", {}).get("verified_percentage", 0) > 5 else "low",
            "recommended_approach": "gradual and discreet" if follower_count > 5000 else "direct engagement",
            "operational_security": [
                "Use authentic-looking personas",
                "Gradual relationship escalation",
                "Avoid public displays of manipulation",
                "Maintain plausible cover stories"
            ]
        }
        
        self.intelligence_data["targeting_vectors"] = vectors
    
    def generate_intelligence_summary(self):
        """Generate comprehensive intelligence summary"""
        print("📊 Generating intelligence summary...")
        
        summary = {
            "target_profile": {},
            "key_vulnerabilities": [],
            "recommended_approach": {},
            "success_probability": {},
            "operational_timeline": {},
            "required_resources": []
        }
        
        # Target profile summary
        account_info = self.raw_data.get('data', {}).get('account_info', {})
        psych_profile = self.intelligence_data.get("psychological_profile", {})
        social_analysis = self.intelligence_data.get("social_network_analysis", {})
        
        summary["target_profile"] = {
            "username": account_info.get("username", "unknown"),
            "full_name": account_info.get("full_name", "unknown"),
            "follower_count": account_info.get("followers_count", 0),
            "account_type": "business" if account_info.get("is_business") else "personal",
            "influence_level": social_analysis.get("influence_metrics", {}).get("influence_level", "unknown"),
            "personality_type": psych_profile.get("personality_traits", {}),
            "primary_interests": list(self.intelligence_data.get("behavioral_profile", {}).get("content_preferences", {}).get("hashtag_patterns", {}).get("hashtag_categories", {}).keys())
        }
        
        # Key vulnerabilities
        vulnerabilities = psych_profile.get("vulnerability_assessment", {})
        for vuln, level in vulnerabilities.items():
            if level in ["high", "medium"]:
                summary["key_vulnerabilities"].append({
                    "vulnerability": vuln,
                    "level": level,
                    "exploitability": "high" if level == "high" else "medium"
                })
        
        # Recommended approach
        targeting_vectors = self.intelligence_data.get("targeting_vectors", {})
        primary_vectors = targeting_vectors.get("primary_vectors", {})
        
        if primary_vectors:
            best_vector = max(primary_vectors.items(), key=lambda x: float(x[1].get("probability", "0%").replace("%", "")))
            summary["recommended_approach"] = {
                "primary_vector": best_vector[0],
                "approach": best_vector[1].get("approach", ""),
                "probability": best_vector[1].get("probability", "unknown"),
                "timeline": best_vector[1].get("timeline", "unknown")
            }
        
        # Overall success probability
        if vulnerabilities.get("financial_motivation") == "high" and vulnerabilities.get("validation_seeking") == "high":
            success_prob = "98%"
        elif vulnerabilities.get("financial_motivation") == "high" or vulnerabilities.get("validation_seeking") == "high":
            success_prob = "85%"
        else:
            success_prob = "65%"
        
        summary["success_probability"] = {
            "overall": success_prob,
            "factors": list(vulnerabilities.keys()),
            "confidence": "high" if len(vulnerabilities) >= 3 else "medium"
        }
        
        # Operational timeline
        summary["operational_timeline"] = {
            "phase_1_attraction": "1-3 weeks",
            "phase_2_dependency": "4-8 weeks",
            "phase_3_exploitation": "8-16 weeks",
            "total_operation": "3-6 months",
            "critical_milestones": [
                "Initial contact and attraction",
                "Trust building and validation",
                "Financial/emotional dependency creation",
                "Data extraction and exploitation"
            ]
        }
        
        # Required resources
        summary["required_resources"] = [
            "Credible wealthy persona with trading background",
            "Luxury lifestyle props and evidence",
            "Financial instruments for dependency creation",
            "Social engineering scripts and templates",
            "Long-term operational security measures"
        ]
        
        self.intelligence_data["intelligence_summary"] = summary
    
    def run_complete_analysis(self):
        """Run complete intelligence analysis"""
        print("🚀 Starting comprehensive intelligence analysis...")
        print("=" * 60)
        
        if not self.raw_data:
            print("❌ No extraction data loaded")
            return
        
        # Run all analysis modules
        self.analyze_behavioral_patterns()
        self.analyze_social_network()
        self.analyze_communication_patterns()
        self.create_psychological_profile()
        self.generate_targeting_vectors()
        self.generate_intelligence_summary()
        
        print("✅ Intelligence analysis completed")
        return self.intelligence_data
    
    def save_intelligence_report(self, filename=None):
        """Save intelligence analysis to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"instagram_intelligence_report_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.intelligence_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Intelligence report saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Failed to save report: {str(e)}")
            return None
    
    def print_summary_report(self):
        """Print formatted summary report"""
        summary = self.intelligence_data.get("intelligence_summary", {})
        
        print("\n" + "="*80)
        print("📊 INSTAGRAM INTELLIGENCE ANALYSIS REPORT")
        print("="*80)
        
        # Target Profile
        profile = summary.get("target_profile", {})
        print(f"\n🎯 TARGET PROFILE:")
        print(f"   • Username: @{profile.get('username', 'unknown')}")
        print(f"   • Full Name: {profile.get('full_name', 'unknown')}")
        print(f"   • Followers: {profile.get('follower_count', 0):,}")
        print(f"   • Account Type: {profile.get('account_type', 'unknown')}")
        print(f"   • Influence Level: {profile.get('influence_level', 'unknown')}")
        print(f"   • Primary Interests: {', '.join(profile.get('primary_interests', []))}")
        
        # Key Vulnerabilities
        vulnerabilities = summary.get("key_vulnerabilities", [])
        print(f"\n🎯 KEY VULNERABILITIES:")
        for vuln in vulnerabilities:
            print(f"   • {vuln['vulnerability']}: {vuln['level']} (exploitability: {vuln['exploitability']})")
        
        # Recommended Approach
        approach = summary.get("recommended_approach", {})
        print(f"\n🎯 RECOMMENDED APPROACH:")
        print(f"   • Primary Vector: {approach.get('primary_vector', 'unknown')}")
        print(f"   • Approach: {approach.get('approach', 'unknown')}")
        print(f"   • Success Probability: {approach.get('probability', 'unknown')}")
        print(f"   • Timeline: {approach.get('timeline', 'unknown')}")
        
        # Success Probability
        success = summary.get("success_probability", {})
        print(f"\n📈 SUCCESS ASSESSMENT:")
        print(f"   • Overall Probability: {success.get('overall', 'unknown')}")
        print(f"   • Confidence Level: {success.get('confidence', 'unknown')}")
        print(f"   • Contributing Factors: {len(success.get('factors', []))}")
        
        # Timeline
        timeline = summary.get("operational_timeline", {})
        print(f"\n⏰ OPERATIONAL TIMELINE:")
        print(f"   • Phase 1 (Attraction): {timeline.get('phase_1_attraction', 'unknown')}")
        print(f"   • Phase 2 (Dependency): {timeline.get('phase_2_dependency', 'unknown')}")
        print(f"   • Phase 3 (Exploitation): {timeline.get('phase_3_exploitation', 'unknown')}")
        print(f"   • Total Operation: {timeline.get('total_operation', 'unknown')}")
        
        print("\n" + "="*80)

def main():
    """Main execution function"""
    print("🧠 Instagram Intelligence Analyzer")
    print("=" * 50)
    
    # Find the most recent extraction file
    extraction_files = [f for f in os.listdir('.') if f.startswith('instagram_') and f.endswith('.json')]
    if extraction_files:
        latest_file = max(extraction_files, key=os.path.getctime)
        print(f"📁 Using latest extraction file: {latest_file}")
        
        # Initialize analyzer
        analyzer = InstagramIntelligenceAnalyzer(latest_file)
        
        # Run analysis
        intelligence_data = analyzer.run_complete_analysis()
        
        # Save report
        report_file = analyzer.save_intelligence_report()
        
        # Print summary
        analyzer.print_summary_report()
        
        print(f"\n💾 Full report saved to: {report_file}")
        
    else:
        print("❌ No extraction files found")
        print("Please run the Instagram extractor first")

if __name__ == "__main__":
    main()
