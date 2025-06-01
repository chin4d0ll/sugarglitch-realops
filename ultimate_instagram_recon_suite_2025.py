#!/usr/bin/env python3
"""
👑🔥 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 2025 🔥👑
===========================================================
- รวม Enhanced Private Bypass + Ultimate Image Analyzer
- Master Controller สำหรับ Instagram OSINT แบบครบครัน
- AI-powered analysis + Advanced reconnaissance
- Real-time monitoring + Comprehensive reporting

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 - Ultimate Master Edition!
For: Educational & Security Research Only!
"""

import asyncio
import json
import time
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import warnings
warnings.filterwarnings("ignore")

# Import our tools
try:
    from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass
    BYPASS_AVAILABLE = True
except ImportError:
    BYPASS_AVAILABLE = False
    print("⚠️ Enhanced Bypass not available")

try:
    from ultimate_image_analyzer_2025 import UltimateImageAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    print("⚠️ Image Analyzer not available")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
👑💖👻 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 👻💖👑
                โดย น้องจิน - Ultimate Master Edition! ♥️
        Enhanced Private Bypass + Ultimate Image Analyzer + AI Analysis
        ครบครันทุกเครื่องมือ Instagram OSINT แบบ Professional!
"""

class UltimateInstagramReconSuite:
    """
    👑 Ultimate Instagram Reconnaissance Suite
    
    ✨ Master Features:
    - Enhanced Private Profile Bypass
    - Ultimate Image Analysis with AI
    - Comprehensive OSINT Gathering
    - Real-time Monitoring
    - Professional Reporting
    - Multi-target Operations
    """
    
    def __init__(self):
        self.suite_id = f"ULTIMATE_RECON_{int(time.time())}"
        self.start_time = time.time()
        
        # Master results storage
        self.master_results = {
            'suite_id': self.suite_id,
            'start_time': datetime.now().isoformat(),
            'targets_processed': [],
            'total_targets': 0,
            'successful_operations': 0,
            'failed_operations': 0,
            'images_analyzed': 0,
            'faces_detected': 0,
            'deepfake_detections': 0,
            'osint_sources_found': 0,
            'cache_sources_found': 0,
            'comprehensive_reports': []
        }
        
        # Initialize components
        self.bypass_tool = None
        self.analyzer_tool = None
        
        if BYPASS_AVAILABLE:
            self.girly_print("✅ Enhanced Private Bypass Ready", "SUCCESS", "🔓")
        
        if ANALYZER_AVAILABLE:
            self.analyzer_tool = UltimateImageAnalyzer()
            self.girly_print("✅ Ultimate Image Analyzer Ready", "SUCCESS", "🎨")

    def girly_print(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """Enhanced girly printing with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[96m",     # Cyan
            "SUCCESS": "\033[92m",  # Green  
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",    # Red
            "CRITICAL": "\033[95m", # Magenta
            "RESET": "\033[0m"      # Reset
        }
        
        color = colors.get(level, colors["INFO"])
        print(f"{color}{emoji} [{timestamp}] {message}{colors['RESET']}")

    async def ultimate_target_reconnaissance(self, target_username: str) -> Dict:
        """
        🎯 Ultimate Target Reconnaissance - การลาดตระเวนแบบครบครัน
        
        Args:
            target_username: Instagram username to investigate
            
        Returns:
            Comprehensive reconnaissance results
        """
        self.girly_print(f"🎯 เริ่ม Ultimate Reconnaissance: @{target_username}", "INFO", "👑")
        
        recon_start = time.time()
        
        recon_results = {
            'target': target_username,
            'recon_id': f"RECON_{target_username}_{int(time.time())}",
            'timestamp': datetime.now().isoformat(),
            'bypass_results': {},
            'image_analysis': {},
            'osint_data': {},
            'security_assessment': {},
            'recommendations': [],
            'success_rate': 0,
            'duration': 0
        }
        
        try:
            # Phase 1: Enhanced Private Bypass
            if BYPASS_AVAILABLE:
                self.girly_print("🔓 Phase 1: Enhanced Private Bypass", "INFO", "⚡")
                
                self.bypass_tool = SuperEnhancedInstagramBypass(target_username)
                bypass_result = await self.bypass_tool.execute_enhanced_bypass()
                
                recon_results['bypass_results'] = bypass_result
                
                if bypass_result.get('success'):
                    self.girly_print("✅ Private Bypass สำเร็จ!", "SUCCESS", "🔥")
                    
                    # Extract image URLs for analysis
                    extracted_data = bypass_result.get('extracted_data', {})
                    image_urls = self.extract_image_urls_from_data(extracted_data)
                    
                    if image_urls:
                        self.girly_print(f"📸 พบรูปภาพ {len(image_urls)} รูป สำหรับวิเคราะห์", "INFO", "🖼️")
                        recon_results['found_images'] = image_urls
                else:
                    self.girly_print("⚠️ Private Bypass บางส่วนสำเร็จ", "WARNING", "😅")
            
            # Phase 2: Image Analysis (if images found)
            if ANALYZER_AVAILABLE and recon_results.get('found_images'):
                self.girly_print("🎨 Phase 2: Ultimate Image Analysis", "INFO", "⚡")
                
                # Download and analyze images
                image_analysis = await self.analyze_target_images(
                    target_username, 
                    recon_results['found_images']
                )
                
                recon_results['image_analysis'] = image_analysis
                
                # Update master stats
                self.master_results['images_analyzed'] += image_analysis.get('total_analyzed', 0)
                self.master_results['faces_detected'] += image_analysis.get('total_faces', 0)
                self.master_results['deepfake_detections'] += image_analysis.get('high_risk_images', 0)
            
            # Phase 3: Advanced OSINT Correlation
            self.girly_print("🕵️ Phase 3: Advanced OSINT Correlation", "INFO", "⚡")
            osint_data = await self.advanced_osint_correlation(target_username, recon_results)
            recon_results['osint_data'] = osint_data
            
            # Phase 4: Security Assessment
            self.girly_print("🛡️ Phase 4: Security Assessment", "INFO", "⚡")
            security_assessment = self.conduct_security_assessment(recon_results)
            recon_results['security_assessment'] = security_assessment
            
            # Phase 5: Generate Recommendations
            self.girly_print("💡 Phase 5: Generating Recommendations", "INFO", "⚡")
            recommendations = self.generate_target_recommendations(recon_results)
            recon_results['recommendations'] = recommendations
            
            # Calculate success metrics
            recon_results['duration'] = round(time.time() - recon_start, 2)
            recon_results['success_rate'] = self.calculate_recon_success_rate(recon_results)
            
            # Update master results
            self.master_results['targets_processed'].append(recon_results)
            self.master_results['total_targets'] += 1
            
            if recon_results['success_rate'] >= 50:
                self.master_results['successful_operations'] += 1
            else:
                self.master_results['failed_operations'] += 1
            
            self.girly_print(f"🎉 Ultimate Reconnaissance Complete! Success: {recon_results['success_rate']:.1f}%", "SUCCESS", "👑")
            
            return recon_results
            
        except Exception as e:
            recon_results['error'] = str(e)
            self.master_results['failed_operations'] += 1
            self.girly_print(f"❌ Reconnaissance failed: {str(e)[:50]}...", "ERROR", "💔")
            return recon_results

    def extract_image_urls_from_data(self, extracted_data: Dict) -> List[str]:
        """
        📸 Extract image URLs from bypass data
        
        Args:
            extracted_data: Data from bypass tool
            
        Returns:
            List of image URLs
        """
        image_urls = []
        
        try:
            # Search for image URLs in extracted data
            data_str = json.dumps(extracted_data, default=str).lower()
            
            # Common Instagram image URL patterns
            import re
            url_patterns = [
                r'https://[^"]*\.cdninstagram\.com/[^"]*\.jpg',
                r'https://[^"]*\.fbcdn\.net/[^"]*\.jpg',
                r'https://scontent[^"]*\.jpg',
                r'"profile_pic_url[^"]*":\s*"([^"]*)"',
                r'"url[^"]*":\s*"([^"]*\.jpg[^"]*)"'
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, data_str, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else match[1] if len(match) > 1 else ""
                    
                    if match and 'jpg' in match.lower() and match not in image_urls:
                        image_urls.append(match)
            
            # Limit to reasonable number
            image_urls = image_urls[:10]
            
            self.girly_print(f"📸 Extracted {len(image_urls)} image URLs", "SUCCESS", "🖼️")
            
        except Exception as e:
            self.girly_print(f"❌ Image URL extraction failed: {e}", "WARNING", "😅")
        
        return image_urls

    async def analyze_target_images(self, target_username: str, image_urls: List[str]) -> Dict:
        """
        🎨 Analyze images for target
        
        Args:
            target_username: Target username
            image_urls: List of image URLs to analyze
            
        Returns:
            Image analysis results
        """
        
        analysis_results = {
            'total_images': len(image_urls),
            'total_analyzed': 0,
            'total_faces': 0,
            'high_risk_images': 0,
            'medium_risk_images': 0,
            'low_risk_images': 0,
            'professional_quality': 0,
            'filter_detected': 0,
            'individual_analyses': []
        }
        
        try:
            # Create download directory
            download_dir = Path(f"downloaded_images_{target_username}_{int(time.time())}")
            download_dir.mkdir(exist_ok=True)
            
            # Download and analyze each image
            for i, url in enumerate(image_urls[:5]):  # Limit to 5 images for performance
                try:
                    # Download image
                    filename = download_dir / f"image_{i+1}.jpg"
                    
                    if self.analyzer_tool.download_image(url, str(filename)):
                        # Analyze image
                        analysis = self.analyzer_tool.analyze_single_image(str(filename), url)
                        analysis_results['individual_analyses'].append(analysis)
                        analysis_results['total_analyzed'] += 1
                        
                        # Aggregate statistics
                        if 'faces' in analysis:
                            analysis_results['total_faces'] += analysis['faces'].get('total_faces', 0)
                        
                        if 'deepfake' in analysis:
                            risk_level = analysis['deepfake'].get('risk_level', 'Low')
                            if risk_level == 'High':
                                analysis_results['high_risk_images'] += 1
                            elif risk_level == 'Medium':
                                analysis_results['medium_risk_images'] += 1
                            else:
                                analysis_results['low_risk_images'] += 1
                        
                        if 'aesthetic' in analysis:
                            instagram_features = analysis['aesthetic'].get('instagram_features', {})
                            if instagram_features.get('professional_quality'):
                                analysis_results['professional_quality'] += 1
                            if instagram_features.get('filter_likelihood') in ['High', 'Medium']:
                                analysis_results['filter_detected'] += 1
                
                except Exception as e:
                    self.girly_print(f"❌ Failed to analyze image {i+1}: {e}", "WARNING", "🖼️")
                    continue
            
            self.girly_print(f"🎨 Image analysis complete: {analysis_results['total_analyzed']}/{analysis_results['total_images']}", "SUCCESS", "✅")
            
        except Exception as e:
            analysis_results['error'] = str(e)
            self.girly_print(f"❌ Image analysis failed: {e}", "ERROR", "💔")
        
        return analysis_results

    async def advanced_osint_correlation(self, target_username: str, recon_data: Dict) -> Dict:
        """
        🕵️ Advanced OSINT correlation and cross-referencing
        
        Args:
            target_username: Target username
            recon_data: Existing reconnaissance data
            
        Returns:
            Correlated OSINT data
        """
        
        osint_results = {
            'correlation_id': f"OSINT_{target_username}_{int(time.time())}",
            'cross_platform_findings': {},
            'data_correlations': {},
            'timeline_analysis': {},
            'behavior_patterns': {},
            'risk_assessment': {}
        }
        
        try:
            # Extract data from bypass results
            bypass_data = recon_data.get('bypass_results', {})
            extracted_data = bypass_data.get('extracted_data', {})
            
            # Cross-platform correlation
            platforms_found = []
            if 'twitter_bio' in extracted_data:
                platforms_found.append('Twitter')
            if 'tiktok_followers' in extracted_data:
                platforms_found.append('TikTok')
            if 'github_bio' in extracted_data:
                platforms_found.append('GitHub')
            if 'pinterest_bio' in extracted_data:
                platforms_found.append('Pinterest')
            
            osint_results['cross_platform_findings'] = {
                'platforms_found': platforms_found,
                'cross_platform_consistency': len(platforms_found) > 1,
                'total_platforms': len(platforms_found)
            }
            
            # Data correlation analysis
            correlations = []
            
            # Username consistency
            if target_username.lower() in str(extracted_data).lower():
                correlations.append('Username consistency across platforms')
            
            # Bio/description analysis
            bio_texts = []
            for key, value in extracted_data.items():
                if 'bio' in key.lower() and value:
                    bio_texts.append(str(value))
            
            if bio_texts:
                # Simple keyword matching
                common_keywords = self.find_common_keywords(bio_texts)
                if common_keywords:
                    correlations.append(f'Common bio keywords: {", ".join(common_keywords[:3])}')
            
            osint_results['data_correlations'] = {
                'correlations_found': correlations,
                'correlation_strength': len(correlations) / 5.0  # Normalize to 0-1
            }
            
            # Timeline analysis (basic)
            osint_results['timeline_analysis'] = {
                'account_age_estimate': 'Unknown',
                'activity_patterns': 'Limited data',
                'posting_frequency': 'Cannot determine'
            }
            
            # Behavior patterns
            behavior_indicators = []
            
            if extracted_data.get('follower_count', 0) > 10000:
                behavior_indicators.append('High follower count - potential influencer')
            
            if extracted_data.get('is_verified'):
                behavior_indicators.append('Verified account - public figure')
            
            if extracted_data.get('is_private'):
                behavior_indicators.append('Private account - privacy conscious')
            
            osint_results['behavior_patterns'] = {
                'indicators': behavior_indicators,
                'privacy_level': 'High' if extracted_data.get('is_private') else 'Low',
                'public_exposure': len(platforms_found)
            }
            
            # Risk assessment
            risk_factors = []
            
            if len(platforms_found) > 3:
                risk_factors.append('High cross-platform exposure')
            
            if not extracted_data.get('is_private'):
                risk_factors.append('Public Instagram profile')
            
            if extracted_data.get('follower_count', 0) > 50000:
                risk_factors.append('High public visibility')
            
            osint_results['risk_assessment'] = {
                'risk_factors': risk_factors,
                'privacy_score': max(0, 10 - len(risk_factors) * 2),  # 0-10 scale
                'exposure_level': 'High' if len(risk_factors) > 2 else 'Medium' if len(risk_factors) > 0 else 'Low'
            }
            
            # Update master stats
            self.master_results['osint_sources_found'] += len(platforms_found)
            
            self.girly_print(f"🕵️ OSINT correlation complete: {len(platforms_found)} platforms, {len(correlations)} correlations", "SUCCESS", "📊")
            
        except Exception as e:
            osint_results['error'] = str(e)
            self.girly_print(f"❌ OSINT correlation failed: {e}", "ERROR", "💔")
        
        return osint_results

    def find_common_keywords(self, texts: List[str]) -> List[str]:
        """Find common keywords across multiple texts"""
        try:
            if len(texts) < 2:
                return []
            
            # Simple keyword extraction
            import re
            all_words = []
            
            for text in texts:
                # Extract words (basic)
                words = re.findall(r'\b\w+\b', text.lower())
                words = [w for w in words if len(w) > 3]  # Filter short words
                all_words.extend(words)
            
            # Find common words
            from collections import Counter
            word_counts = Counter(all_words)
            common_words = [word for word, count in word_counts.items() if count >= 2]
            
            return common_words[:5]  # Top 5 common words
            
        except:
            return []

    def conduct_security_assessment(self, recon_results: Dict) -> Dict:
        """
        🛡️ Conduct comprehensive security assessment
        
        Args:
            recon_results: Complete reconnaissance results
            
        Returns:
            Security assessment
        """
        
        assessment = {
            'assessment_id': f"SEC_{int(time.time())}",
            'overall_security_score': 0,
            'vulnerability_analysis': {},
            'privacy_evaluation': {},
            'exposure_metrics': {},
            'threat_indicators': [],
            'recommendations': []
        }
        
        try:
            # Privacy evaluation
            bypass_data = recon_results.get('bypass_results', {})
            extracted_data = bypass_data.get('extracted_data', {})
            
            privacy_score = 10  # Start with maximum privacy
            
            # Deduct points for exposure
            if not extracted_data.get('is_private'):
                privacy_score -= 3
                assessment['threat_indicators'].append('Public Instagram profile')
            
            # Check cross-platform exposure
            osint_data = recon_results.get('osint_data', {})
            platforms_found = osint_data.get('cross_platform_findings', {}).get('total_platforms', 0)
            
            if platforms_found > 3:
                privacy_score -= 2
                assessment['threat_indicators'].append('High cross-platform exposure')
            elif platforms_found > 1:
                privacy_score -= 1
            
            # Image analysis risks
            image_analysis = recon_results.get('image_analysis', {})
            high_risk_images = image_analysis.get('high_risk_images', 0)
            
            if high_risk_images > 0:
                privacy_score -= 2
                assessment['threat_indicators'].append(f'{high_risk_images} high-risk images detected')
            
            # Face detection exposure
            total_faces = image_analysis.get('total_faces', 0)
            if total_faces > 0:
                privacy_score -= 1
                assessment['threat_indicators'].append(f'{total_faces} faces detected in images')
            
            assessment['privacy_evaluation'] = {
                'privacy_score': max(0, privacy_score),
                'privacy_level': 'High' if privacy_score >= 7 else 'Medium' if privacy_score >= 4 else 'Low',
                'major_concerns': len([t for t in assessment['threat_indicators'] if 'high' in t.lower() or 'public' in t.lower()])
            }
            
            # Vulnerability analysis
            vulnerabilities = []
            
            if bypass_data.get('success'):
                vulnerabilities.append('Profile data extractable via cache methods')
            
            if image_analysis.get('total_analyzed', 0) > 0:
                vulnerabilities.append('Images accessible for analysis')
            
            if platforms_found > 2:
                vulnerabilities.append('Multiple platform correlation possible')
            
            assessment['vulnerability_analysis'] = {
                'vulnerabilities_found': vulnerabilities,
                'vulnerability_count': len(vulnerabilities),
                'severity': 'High' if len(vulnerabilities) > 2 else 'Medium' if len(vulnerabilities) > 0 else 'Low'
            }
            
            # Exposure metrics
            assessment['exposure_metrics'] = {
                'data_extractability': bypass_data.get('success', False),
                'image_accessibility': image_analysis.get('total_analyzed', 0) > 0,
                'cross_platform_presence': platforms_found,
                'public_information_score': 10 - privacy_score
            }
            
            # Overall security score (0-100)
            assessment['overall_security_score'] = max(0, min(100, privacy_score * 10 - len(vulnerabilities) * 5))
            
            self.girly_print(f"🛡️ Security assessment complete: Score {assessment['overall_security_score']}/100", "SUCCESS", "📊")
            
        except Exception as e:
            assessment['error'] = str(e)
            self.girly_print(f"❌ Security assessment failed: {e}", "ERROR", "💔")
        
        return assessment

    def generate_target_recommendations(self, recon_results: Dict) -> List[str]:
        """
        💡 Generate actionable recommendations based on reconnaissance
        
        Args:
            recon_results: Complete reconnaissance results
            
        Returns:
            List of recommendations
        """
        
        recommendations = []
        
        try:
            security_assessment = recon_results.get('security_assessment', {})
            privacy_score = security_assessment.get('privacy_evaluation', {}).get('privacy_score', 5)
            
            # Privacy recommendations
            if privacy_score < 5:
                recommendations.append("🔒 CRITICAL: Improve privacy settings immediately")
                recommendations.append("📱 Consider making Instagram account private")
                recommendations.append("🚫 Limit cross-platform username correlation")
            elif privacy_score < 7:
                recommendations.append("⚠️ Review and strengthen privacy settings")
                recommendations.append("🔍 Audit public information exposure")
            
            # Image-based recommendations
            image_analysis = recon_results.get('image_analysis', {})
            
            if image_analysis.get('total_faces', 0) > 0:
                recommendations.append("👥 Consider reducing face visibility in public images")
            
            if image_analysis.get('high_risk_images', 0) > 0:
                recommendations.append("🤖 Review images flagged as potential deepfake risks")
            
            # OSINT recommendations
            osint_data = recon_results.get('osint_data', {})
            platforms_found = osint_data.get('cross_platform_findings', {}).get('total_platforms', 0)
            
            if platforms_found > 3:
                recommendations.append("🌐 Reduce cross-platform information correlation")
                recommendations.append("🔄 Use different usernames across platforms")
            
            # General security recommendations
            recommendations.extend([
                "📊 Regular privacy audits recommended",
                "🛡️ Monitor digital footprint periodically",
                "📋 Review EXIF data before posting images",
                "⚠️ Be aware of cached data persistence"
            ])
            
            # Limit to most important recommendations
            return recommendations[:8]
            
        except Exception as e:
            return [f"❌ Recommendation generation failed: {e}"]

    def calculate_recon_success_rate(self, recon_results: Dict) -> float:
        """Calculate overall reconnaissance success rate"""
        
        try:
            success_points = 0
            total_points = 0
            
            # Bypass success (40 points)
            total_points += 40
            if recon_results.get('bypass_results', {}).get('success'):
                success_points += 40
            
            # Image analysis success (30 points)
            total_points += 30
            images_analyzed = recon_results.get('image_analysis', {}).get('total_analyzed', 0)
            total_images = recon_results.get('image_analysis', {}).get('total_images', 0)
            if total_images > 0:
                success_points += (images_analyzed / total_images) * 30
            
            # OSINT correlation success (20 points)
            total_points += 20
            platforms_found = recon_results.get('osint_data', {}).get('cross_platform_findings', {}).get('total_platforms', 0)
            if platforms_found > 0:
                success_points += min(platforms_found / 3, 1.0) * 20
            
            # Security assessment success (10 points)
            total_points += 10
            if 'security_assessment' in recon_results and 'error' not in recon_results['security_assessment']:
                success_points += 10
            
            return (success_points / total_points) * 100 if total_points > 0 else 0
            
        except:
            return 0

    def generate_master_report(self) -> str:
        """
        📋 Generate comprehensive master report
        
        Returns:
            Formatted master report
        """
        
        end_time = time.time()
        total_duration = round(end_time - self.start_time, 2)
        
        report = f"""
👑🔥 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE - MASTER REPORT 🔥👑
{'='*90}

📊 MASTER SUITE SUMMARY
Suite ID: {self.suite_id}
Session Duration: {total_duration} seconds
Start Time: {self.master_results['start_time']}
End Time: {datetime.now().isoformat()}

🎯 OPERATION STATISTICS
Total Targets Processed: {self.master_results['total_targets']}
Successful Operations: {self.master_results['successful_operations']}
Failed Operations: {self.master_results['failed_operations']}
Success Rate: {(self.master_results['successful_operations']/max(1, self.master_results['total_targets'])*100):.1f}%

📸 IMAGE ANALYSIS SUMMARY
Total Images Analyzed: {self.master_results['images_analyzed']}
Faces Detected: {self.master_results['faces_detected']}
Deepfake Detections: {self.master_results['deepfake_detections']}

🕵️ OSINT INTELLIGENCE
OSINT Sources Found: {self.master_results['osint_sources_found']}
Cache Sources Found: {self.master_results['cache_sources_found']}

"""
        
        # Individual target summaries
        if self.master_results['targets_processed']:
            report += "🎯 TARGET SUMMARIES\n"
            
            for i, target in enumerate(self.master_results['targets_processed'], 1):
                target_name = target.get('target', 'Unknown')
                success_rate = target.get('success_rate', 0)
                duration = target.get('duration', 0)
                
                report += f"""
Target {i}: @{target_name}
  • Success Rate: {success_rate:.1f}%
  • Duration: {duration} seconds
  • Images Analyzed: {target.get('image_analysis', {}).get('total_analyzed', 0)}
  • Platforms Found: {target.get('osint_data', {}).get('cross_platform_findings', {}).get('total_platforms', 0)}
  • Security Score: {target.get('security_assessment', {}).get('overall_security_score', 'N/A')}/100
"""
        
        # Overall recommendations
        report += f"""
💡 MASTER RECOMMENDATIONS
Based on {self.master_results['total_targets']} target(s) analyzed:

"""
        
        if self.master_results['successful_operations'] > 0:
            report += """✅ SUCCESSFUL OPERATIONS:
  • Reconnaissance techniques are effective
  • Consider implementing regular monitoring
  • Cross-reference findings with additional sources
  • Maintain updated privacy recommendations

"""
        
        if self.master_results['failed_operations'] > 0:
            report += """⚠️ FAILED OPERATIONS:
  • Some targets have strong privacy protection
  • Consider alternative reconnaissance methods
  • Update techniques for better success rates
  • Focus on publicly available information

"""
        
        # Performance insights
        if self.master_results['total_targets'] > 0:
            avg_duration = total_duration / self.master_results['total_targets']
            report += f"""📈 PERFORMANCE INSIGHTS:
  • Average time per target: {avg_duration:.1f} seconds
  • Images analyzed per target: {self.master_results['images_analyzed']/self.master_results['total_targets']:.1f}
  • Face detection rate: {(self.master_results['faces_detected']/max(1, self.master_results['images_analyzed'])*100):.1f}%
  • Deepfake detection rate: {(self.master_results['deepfake_detections']/max(1, self.master_results['images_analyzed'])*100):.1f}%

"""
        
        report += f"""🏆 SUITE CAPABILITIES DEMONSTRATED:
✅ Enhanced Private Profile Bypass
✅ Ultimate AI Image Analysis
✅ Advanced OSINT Correlation
✅ Comprehensive Security Assessment
✅ Professional Intelligence Reporting

💖 Generated by น้องจิน's Ultimate Instagram Reconnaissance Suite
👻 For educational and security research only!
🔥 Master Report ID: {self.suite_id}_{int(time.time())}

⚠️ DISCLAIMER: Use responsibly and ethically!
All operations performed for educational and legitimate security research purposes only.
"""
        
        return report

    async def run_interactive_mode(self):
        """
        🎮 Interactive mode for Ultimate Reconnaissance Suite
        """
        
        while True:
            print("\n👑 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 👑")
            print("1. 🎯 Single Target Reconnaissance")
            print("2. 📋 Multiple Target Analysis")
            print("3. 🔍 Quick Bypass Only")
            print("4. 🎨 Quick Image Analysis Only")
            print("5. 📊 View Master Report")
            print("0. 💔 Exit")
            
            choice = input("\n💖 เลือกเมนู (0-5): ").strip()
            
            try:
                if choice == '1':
                    # Single target reconnaissance
                    username = input("🎯 Instagram username (without @): ").strip()
                    if username:
                        result = await self.ultimate_target_reconnaissance(username)
                        
                        # Save individual report
                        timestamp = int(time.time())
                        report_file = Path(f"ultimate_recon_{username}_{timestamp}.json")
                        with open(report_file, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2, default=str)
                        
                        self.girly_print(f"📋 Individual report saved: {report_file.name}", "SUCCESS", "💾")
                
                elif choice == '2':
                    # Multiple target analysis
                    usernames_input = input("📋 Username list (comma-separated): ").strip()
                    if usernames_input:
                        usernames = [u.strip() for u in usernames_input.split(',')]
                        
                        for username in usernames[:5]:  # Limit to 5 targets
                            if username:
                                self.girly_print(f"🎯 Processing target: @{username}", "INFO", "🔄")
                                await self.ultimate_target_reconnaissance(username)
                        
                        # Generate and save master report
                        master_report = self.generate_master_report()
                        print(master_report)
                        
                        timestamp = int(time.time())
                        master_file = Path(f"ultimate_master_report_{timestamp}.txt")
                        with open(master_file, 'w', encoding='utf-8') as f:
                            f.write(master_report)
                        
                        self.girly_print(f"📋 Master report saved: {master_file.name}", "SUCCESS", "💾")
                
                elif choice == '3':
                    # Quick bypass only
                    if BYPASS_AVAILABLE:
                        username = input("🔍 Instagram username: ").strip()
                        if username:
                            bypass_tool = SuperEnhancedInstagramBypass(username)
                            result = await bypass_tool.execute_enhanced_bypass()
                            print(f"🔓 Bypass success: {result.get('success', False)}")
                    else:
                        self.girly_print("❌ Enhanced Bypass not available", "ERROR", "💔")
                
                elif choice == '4':
                    # Quick image analysis only
                    if ANALYZER_AVAILABLE:
                        image_path = input("🎨 Image file path: ").strip()
                        if image_path and Path(image_path).exists():
                            result = self.analyzer_tool.analyze_single_image(image_path)
                            print(f"🎨 Analysis complete: {result.get('analysis_id', 'Unknown')}")
                    else:
                        self.girly_print("❌ Image Analyzer not available", "ERROR", "💔")
                
                elif choice == '5':
                    # View master report
                    master_report = self.generate_master_report()
                    print(master_report)
                
                elif choice == '0':
                    # Generate final master report before exit
                    if self.master_results['total_targets'] > 0:
                        self.girly_print("📊 Generating final master report...", "INFO", "📋")
                        master_report = self.generate_master_report()
                        
                        timestamp = int(time.time())
                        final_file = Path(f"ultimate_final_report_{timestamp}.txt")
                        with open(final_file, 'w', encoding='utf-8') as f:
                            f.write(master_report)
                        
                        self.girly_print(f"📋 Final report saved: {final_file.name}", "SUCCESS", "💾")
                    
                    print("👋 บาย! ใช้งานให้เป็นประโยชน์นะคะ ♥️")
                    break
                
                else:
                    print("❌ เลือกเมนูให้ถูกนะคะ")
                    
            except KeyboardInterrupt:
                print("\n⚠️ หยุดการทำงาน")
            except Exception as e:
                self.girly_print(f"❌ Error: {e}", "ERROR", "💔")

def main():
    """Main function"""
    print(GIRLY_BANNER)
    
    # Check component availability
    if not BYPASS_AVAILABLE:
        print("⚠️ Enhanced Private Bypass not available - some features will be limited")
    
    if not ANALYZER_AVAILABLE:
        print("⚠️ Ultimate Image Analyzer not available - image analysis will be limited")
    
    if not BYPASS_AVAILABLE and not ANALYZER_AVAILABLE:
        print("❌ No components available. Please check installations.")
        return
    
    # Initialize and run suite
    suite = UltimateInstagramReconSuite()
    
    try:
        asyncio.run(suite.run_interactive_mode())
    except KeyboardInterrupt:
        print("\n⚠️ Suite interrupted by user")
    except Exception as e:
        print(f"❌ Suite error: {e}")

if __name__ == "__main__":
    main()
