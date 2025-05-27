#!/usr/bin/env python3
"""
🕸️ PHASE 3: NETWORK ANALYSIS & BEHAVIORAL PROFILING
Advanced relationship mapping and pattern recognition
Target: alx.trading | Password: Fleming654
"""

import json
import time
import random
import sys
import os
from datetime import datetime, timedelta
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import sqlite3
import re
from textblob import TextBlob
import hashlib

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class InstagramNetworkAnalyzer:
    def __init__(self, target_username="alx.trading"):
        self.target = target_username
        self.database_file = f"instagram_deep_data_{target_username}.db"
        self.network_graph = nx.Graph()
        
        self.analysis_results = {
            "network_metrics": {},
            "behavioral_patterns": {},
            "content_analysis": {},
            "temporal_patterns": {},
            "relationship_insights": {},
            "risk_assessment": {},
            "prediction_models": {}
        }
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def load_database_data(self):
        """Load data from SQLite database"""
        try:
            safe_print("🗄️ Loading deep mining data from database...")
            
            if not os.path.exists(self.database_file):
                safe_print("⚠️ Database not found - running basic analysis")
                return False
            
            conn = sqlite3.connect(self.database_file)
            
            # Load different data types
            self.profile_data = pd.read_sql_query("SELECT * FROM profile_data", conn)
            self.posts_data = pd.read_sql_query("SELECT * FROM posts", conn)
            
            try:
                self.followers_data = pd.read_sql_query("SELECT * FROM followers", conn)
                self.following_data = pd.read_sql_query("SELECT * FROM following", conn)
            except:
                self.followers_data = pd.DataFrame()
                self.following_data = pd.DataFrame()
            
            conn.close()
            
            safe_print(f"✅ Loaded: {len(self.posts_data)} posts, {len(self.followers_data)} followers, {len(self.following_data)} following")
            return True
            
        except Exception as e:
            safe_print(f"❌ Database load failed: {e}")
            return False
    
    def analyze_network_structure(self):
        """Analyze network structure and relationships"""
        try:
            safe_print("🕸️ Analyzing network structure...")
            
            # Create network graph
            self.network_graph.add_node(self.target, node_type="target", centrality=1.0)
            
            # Add followers as nodes
            if not self.followers_data.empty:
                for _, follower in self.followers_data.iterrows():
                    self.network_graph.add_node(
                        follower['username'], 
                        node_type="follower",
                        verified=follower.get('is_verified', False),
                        follower_count=follower.get('follower_count', 0)
                    )
                    self.network_graph.add_edge(self.target, follower['username'], relationship="followed_by")
            
            # Add following as nodes
            if not self.following_data.empty:
                for _, following in self.following_data.iterrows():
                    if following['username'] not in self.network_graph:
                        self.network_graph.add_node(
                            following['username'],
                            node_type="following",
                            verified=following.get('is_verified', False),
                            follower_count=following.get('follower_count', 0)
                        )
                    self.network_graph.add_edge(self.target, following['username'], relationship="follows")
            
            # Calculate network metrics
            metrics = {
                "total_nodes": len(self.network_graph.nodes()),
                "total_edges": len(self.network_graph.edges()),
                "network_density": nx.density(self.network_graph),
                "clustering_coefficient": nx.clustering(self.network_graph, self.target) if self.target in self.network_graph else 0
            }
            
            # Calculate centrality measures
            if len(self.network_graph.nodes()) > 1:
                try:
                    degree_centrality = nx.degree_centrality(self.network_graph)
                    betweenness_centrality = nx.betweenness_centrality(self.network_graph)
                    closeness_centrality = nx.closeness_centrality(self.network_graph)
                    
                    metrics["target_degree_centrality"] = degree_centrality.get(self.target, 0)
                    metrics["target_betweenness_centrality"] = betweenness_centrality.get(self.target, 0)
                    metrics["target_closeness_centrality"] = closeness_centrality.get(self.target, 0)
                except:
                    pass
            
            # Identify influential connections
            influential_followers = []
            if not self.followers_data.empty:
                top_followers = self.followers_data.nlargest(10, 'follower_count')
                for _, follower in top_followers.iterrows():
                    influential_followers.append({
                        "username": follower['username'],
                        "follower_count": follower['follower_count'],
                        "is_verified": follower.get('is_verified', False)
                    })
            
            metrics["influential_followers"] = influential_followers
            
            self.analysis_results["network_metrics"] = metrics
            safe_print(f"✅ Network analysis complete: {metrics['total_nodes']} nodes, {metrics['total_edges']} edges")
            
        except Exception as e:
            safe_print(f"❌ Network analysis failed: {e}")
    
    def analyze_content_patterns(self):
        """Analyze content patterns and themes"""
        try:
            safe_print("📝 Analyzing content patterns...")
            
            if self.posts_data.empty:
                safe_print("⚠️ No posts data available")
                return
            
            content_analysis = {
                "total_posts": len(self.posts_data),
                "posts_with_captions": 0,
                "average_caption_length": 0,
                "total_likes": 0,
                "total_comments": 0,
                "hashtag_frequency": {},
                "mention_frequency": {},
                "sentiment_analysis": {},
                "content_themes": {}
            }
            
            all_hashtags = []
            all_mentions = []
            all_captions = []
            
            for _, post in self.posts_data.iterrows():
                # Caption analysis
                if pd.notna(post.get('caption')):
                    content_analysis["posts_with_captions"] += 1
                    caption = str(post['caption'])
                    all_captions.append(caption)
                    
                    # Extract hashtags and mentions
                    if pd.notna(post.get('hashtags')):
                        try:
                            hashtags = json.loads(post['hashtags'])
                            all_hashtags.extend(hashtags)
                        except:
                            hashtags = re.findall(r'#\w+', caption)
                            all_hashtags.extend(hashtags)
                    
                    if pd.notna(post.get('mentions')):
                        try:
                            mentions = json.loads(post['mentions'])
                            all_mentions.extend(mentions)
                        except:
                            mentions = re.findall(r'@\w+', caption)
                            all_mentions.extend(mentions)
                
                # Engagement metrics
                if pd.notna(post.get('likes_count')):
                    content_analysis["total_likes"] += int(post['likes_count'])
                
                if pd.notna(post.get('comments_count')):
                    content_analysis["total_comments"] += int(post['comments_count'])
            
            # Calculate averages
            if content_analysis["posts_with_captions"] > 0:
                total_caption_length = sum(len(caption) for caption in all_captions)
                content_analysis["average_caption_length"] = total_caption_length / content_analysis["posts_with_captions"]
            
            # Frequency analysis
            content_analysis["hashtag_frequency"] = dict(Counter(all_hashtags).most_common(20))
            content_analysis["mention_frequency"] = dict(Counter(all_mentions).most_common(20))
            
            # Sentiment analysis
            if all_captions:
                sentiments = []
                for caption in all_captions[:10]:  # Analyze first 10 captions
                    try:
                        blob = TextBlob(caption)
                        sentiments.append(blob.sentiment.polarity)
                    except:
                        continue
                
                if sentiments:
                    content_analysis["sentiment_analysis"] = {
                        "average_sentiment": np.mean(sentiments),
                        "sentiment_variance": np.var(sentiments),
                        "positive_posts": len([s for s in sentiments if s > 0.1]),
                        "negative_posts": len([s for s in sentiments if s < -0.1]),
                        "neutral_posts": len([s for s in sentiments if -0.1 <= s <= 0.1])
                    }
            
            # Content themes analysis
            trading_keywords = ['trading', 'forex', 'crypto', 'investment', 'profit', 'market', 'trade', 'money', 'financial']
            trading_mentions = 0
            
            for caption in all_captions:
                caption_lower = caption.lower()
                for keyword in trading_keywords:
                    if keyword in caption_lower:
                        trading_mentions += 1
                        break
            
            content_analysis["content_themes"] = {
                "trading_related_posts": trading_mentions,
                "trading_percentage": (trading_mentions / len(all_captions) * 100) if all_captions else 0
            }
            
            self.analysis_results["content_analysis"] = content_analysis
            safe_print(f"✅ Content analysis complete: {content_analysis['total_posts']} posts analyzed")
            
        except Exception as e:
            safe_print(f"❌ Content analysis failed: {e}")
    
    def analyze_temporal_patterns(self):
        """Analyze posting patterns and timing"""
        try:
            safe_print("⏰ Analyzing temporal patterns...")
            
            if self.posts_data.empty:
                safe_print("⚠️ No posts data for temporal analysis")
                return
            
            temporal_analysis = {
                "posting_frequency": {},
                "peak_hours": {},
                "weekly_patterns": {},
                "engagement_timing": {}
            }
            
            # Parse timestamps
            timestamps = []
            for _, post in self.posts_data.iterrows():
                if pd.notna(post.get('timestamp')):
                    try:
                        timestamp = pd.to_datetime(post['timestamp'])
                        timestamps.append(timestamp)
                    except:
                        continue
            
            if timestamps:
                # Daily patterns
                hours = [ts.hour for ts in timestamps]
                hour_counts = Counter(hours)
                temporal_analysis["peak_hours"] = dict(hour_counts.most_common(5))
                
                # Weekly patterns
                weekdays = [ts.strftime('%A') for ts in timestamps]
                weekday_counts = Counter(weekdays)
                temporal_analysis["weekly_patterns"] = dict(weekday_counts)
                
                # Posting frequency (posts per day)
                if len(timestamps) > 1:
                    date_range = (max(timestamps) - min(timestamps)).days
                    if date_range > 0:
                        temporal_analysis["posting_frequency"] = {
                            "posts_per_day": len(timestamps) / date_range,
                            "total_days": date_range,
                            "first_post": min(timestamps).isoformat(),
                            "last_post": max(timestamps).isoformat()
                        }
            
            self.analysis_results["temporal_patterns"] = temporal_analysis
            safe_print(f"✅ Temporal analysis complete: {len(timestamps)} timestamps analyzed")
            
        except Exception as e:
            safe_print(f"❌ Temporal analysis failed: {e}")
    
    def assess_security_risk(self):
        """Assess security risk and behavioral indicators"""
        try:
            safe_print("🛡️ Conducting security risk assessment...")
            
            risk_factors = {
                "account_exposure": "low",
                "content_sensitivity": "medium",
                "network_risk": "low",
                "behavioral_anomalies": [],
                "risk_score": 0,
                "recommendations": []
            }
            
            # Check account exposure
            if not self.profile_data.empty:
                profile = self.profile_data.iloc[0]
                
                if profile.get('is_verified', False):
                    risk_factors["account_exposure"] = "high"
                    risk_factors["risk_score"] += 3
                    risk_factors["recommendations"].append("Verified account - high visibility")
                
                if not profile.get('is_private', True):
                    risk_factors["risk_score"] += 2
                    risk_factors["recommendations"].append("Public account increases exposure")
                
                follower_count = profile.get('follower_count', 0)
                if follower_count > 10000:
                    risk_factors["account_exposure"] = "high"
                    risk_factors["risk_score"] += 2
                elif follower_count > 1000:
                    risk_factors["account_exposure"] = "medium"
                    risk_factors["risk_score"] += 1
            
            # Analyze content sensitivity
            content_analysis = self.analysis_results.get("content_analysis", {})
            if content_analysis:
                trading_percentage = content_analysis.get("content_themes", {}).get("trading_percentage", 0)
                if trading_percentage > 50:
                    risk_factors["content_sensitivity"] = "high"
                    risk_factors["risk_score"] += 2
                    risk_factors["recommendations"].append("High financial content exposure")
            
            # Network risk assessment
            network_metrics = self.analysis_results.get("network_metrics", {})
            if network_metrics:
                influential_followers = network_metrics.get("influential_followers", [])
                verified_followers = len([f for f in influential_followers if f.get("is_verified", False)])
                
                if verified_followers > 5:
                    risk_factors["network_risk"] = "high"
                    risk_factors["risk_score"] += 2
                elif verified_followers > 2:
                    risk_factors["network_risk"] = "medium"
                    risk_factors["risk_score"] += 1
            
            # Determine overall risk level
            if risk_factors["risk_score"] >= 7:
                risk_factors["overall_risk"] = "high"
            elif risk_factors["risk_score"] >= 4:
                risk_factors["overall_risk"] = "medium"
            else:
                risk_factors["overall_risk"] = "low"
            
            self.analysis_results["risk_assessment"] = risk_factors
            safe_print(f"✅ Risk assessment complete: {risk_factors['overall_risk']} risk (score: {risk_factors['risk_score']})")
            
        except Exception as e:
            safe_print(f"❌ Risk assessment failed: {e}")
    
    def generate_behavioral_profile(self):
        """Generate comprehensive behavioral profile"""
        try:
            safe_print("🧠 Generating behavioral profile...")
            
            profile = {
                "account_characteristics": {},
                "content_behavior": {},
                "social_behavior": {},
                "risk_indicators": {},
                "predictive_insights": {}
            }
            
            # Account characteristics
            if not self.profile_data.empty:
                account_data = self.profile_data.iloc[0]
                profile["account_characteristics"] = {
                    "account_age_indicators": "established" if account_data.get('posts_count', 0) > 50 else "new",
                    "engagement_ratio": account_data.get('follower_count', 0) / max(account_data.get('following_count', 1), 1),
                    "verification_status": account_data.get('is_verified', False),
                    "business_account": account_data.get('is_business', False),
                    "privacy_setting": "private" if account_data.get('is_private', False) else "public"
                }
            
            # Content behavior patterns
            content_data = self.analysis_results.get("content_analysis", {})
            if content_data:
                profile["content_behavior"] = {
                    "posting_consistency": "regular" if content_data.get("total_posts", 0) > 20 else "irregular",
                    "caption_usage": content_data.get("posts_with_captions", 0) / max(content_data.get("total_posts", 1), 1),
                    "hashtag_usage": len(content_data.get("hashtag_frequency", {})),
                    "mention_activity": len(content_data.get("mention_frequency", {})),
                    "content_focus": "trading/finance" if content_data.get("content_themes", {}).get("trading_percentage", 0) > 30 else "general"
                }
            
            # Social behavior
            network_data = self.analysis_results.get("network_metrics", {})
            if network_data:
                profile["social_behavior"] = {
                    "network_size": network_data.get("total_nodes", 0),
                    "social_influence": "high" if len(network_data.get("influential_followers", [])) > 3 else "low",
                    "connection_strategy": "selective" if network_data.get("network_density", 0) < 0.1 else "broad"
                }
            
            # Risk indicators
            risk_data = self.analysis_results.get("risk_assessment", {})
            if risk_data:
                profile["risk_indicators"] = {
                    "exposure_level": risk_data.get("overall_risk", "unknown"),
                    "security_score": 10 - risk_data.get("risk_score", 0),
                    "vulnerability_factors": len(risk_data.get("recommendations", []))
                }
            
            # Predictive insights
            profile["predictive_insights"] = {
                "likely_online_hours": list(self.analysis_results.get("temporal_patterns", {}).get("peak_hours", {}).keys())[:3],
                "content_prediction": "financial/trading focus" if profile.get("content_behavior", {}).get("content_focus") == "trading/finance" else "general content",
                "engagement_prediction": "high" if profile.get("account_characteristics", {}).get("engagement_ratio", 0) > 2 else "moderate"
            }
            
            self.analysis_results["behavioral_patterns"] = profile
            safe_print("✅ Behavioral profile generated")
            
        except Exception as e:
            safe_print(f"❌ Behavioral profiling failed: {e}")
    
    def save_analysis_results(self):
        """Save comprehensive analysis results"""
        try:
            # Save JSON results
            filename = f"phase3_network_analysis_{self.target}_{self.timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
            
            # Generate comprehensive report
            report_filename = f"phase3_intelligence_report_{self.target}_{self.timestamp}.md"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(f"# 🕸️ PHASE 3 INTELLIGENCE REPORT\n")
                f.write(f"## Target: {self.target}\n")
                f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Network Analysis
                f.write("## 🕸️ NETWORK ANALYSIS\n")
                network_metrics = self.analysis_results.get("network_metrics", {})
                if network_metrics:
                    f.write(f"- **Total Connections**: {network_metrics.get('total_nodes', 0)}\n")
                    f.write(f"- **Network Density**: {network_metrics.get('network_density', 0):.3f}\n")
                    f.write(f"- **Influential Followers**: {len(network_metrics.get('influential_followers', []))}\n\n")
                
                # Content Analysis
                f.write("## 📝 CONTENT ANALYSIS\n")
                content_analysis = self.analysis_results.get("content_analysis", {})
                if content_analysis:
                    f.write(f"- **Total Posts**: {content_analysis.get('total_posts', 0)}\n")
                    f.write(f"- **Total Likes**: {content_analysis.get('total_likes', 0)}\n")
                    f.write(f"- **Trading Content**: {content_analysis.get('content_themes', {}).get('trading_percentage', 0):.1f}%\n\n")
                
                # Behavioral Profile
                f.write("## 🧠 BEHAVIORAL PROFILE\n")
                behavioral_patterns = self.analysis_results.get("behavioral_patterns", {})
                if behavioral_patterns:
                    f.write(f"- **Account Type**: {behavioral_patterns.get('account_characteristics', {}).get('account_age_indicators', 'unknown')}\n")
                    f.write(f"- **Content Focus**: {behavioral_patterns.get('content_behavior', {}).get('content_focus', 'unknown')}\n")
                    f.write(f"- **Social Influence**: {behavioral_patterns.get('social_behavior', {}).get('social_influence', 'unknown')}\n\n")
                
                # Risk Assessment
                f.write("## 🛡️ RISK ASSESSMENT\n")
                risk_assessment = self.analysis_results.get("risk_assessment", {})
                if risk_assessment:
                    f.write(f"- **Overall Risk Level**: {risk_assessment.get('overall_risk', 'unknown').upper()}\n")
                    f.write(f"- **Risk Score**: {risk_assessment.get('risk_score', 0)}/10\n")
                    f.write(f"- **Security Recommendations**: {len(risk_assessment.get('recommendations', []))}\n\n")
                
                f.write("---\n")
                f.write("*Generated by Phase 3 Network Analysis System*\n")
            
            safe_print(f"💾 Analysis results saved: {filename}")
            safe_print(f"📄 Intelligence report saved: {report_filename}")
            
            return filename, report_filename
            
        except Exception as e:
            safe_print(f"❌ Results save failed: {e}")
            return None, None
    
    def run_network_analysis(self):
        """Execute complete network analysis"""
        safe_print("🕸️ STARTING PHASE 3 NETWORK ANALYSIS")
        safe_print("=" * 60)
        safe_print(f"🎯 Target: {self.target}")
        safe_print(f"📊 Analysis Type: Network & Behavioral")
        safe_print(f"⏰ Timestamp: {self.timestamp}")
        safe_print("=" * 60)
        
        try:
            # Load data
            data_loaded = self.load_database_data()
            
            # Run analysis phases
            safe_print("\n🔍 PHASE 3A: Network Structure Analysis")
            self.analyze_network_structure()
            
            safe_print("\n🔍 PHASE 3B: Content Pattern Analysis")
            self.analyze_content_patterns()
            
            safe_print("\n🔍 PHASE 3C: Temporal Pattern Analysis")
            self.analyze_temporal_patterns()
            
            safe_print("\n🔍 PHASE 3D: Security Risk Assessment")
            self.assess_security_risk()
            
            safe_print("\n🔍 PHASE 3E: Behavioral Profiling")
            self.generate_behavioral_profile()
            
            # Save results
            safe_print("\n💾 PHASE 3F: Results Compilation")
            self.save_analysis_results()
            
            safe_print("\n🎉 PHASE 3 NETWORK ANALYSIS COMPLETE!")
            safe_print("=" * 60)
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Network analysis failed: {e}")
            return False

def main():
    """Execute Phase 3 network analysis"""
    analyzer = InstagramNetworkAnalyzer()
    success = analyzer.run_network_analysis()
    
    if success:
        safe_print("✅ Phase 3 network analysis completed successfully!")
    else:
        safe_print("❌ Phase 3 network analysis failed!")

if __name__ == "__main__":
    main()
