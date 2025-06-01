#!/usr/bin/env python3
"""
🎯📊 DM INTELLIGENCE DASHBOARD 2025 📊🎯
=======================================
- Advanced DM analytics dashboard
- Real-time conversation monitoring
- AI-powered insights
- Interactive data visualization
- Pattern recognition system
- Behavior analysis

แดชบอร์ดวิเคราะห์ DM ขั้นสูงด้วย AI Intelligence!

Created by: น้องจิน (chin4d0ll) ♥️
For: Ultimate Instagram Intelligence Operations 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import json
from datetime import datetime, timedelta
import asyncio
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# Import our extreme extractor
try:
    from extreme_dm_intelligence_extractor_2025 import ExtremeDMIntelligenceExtractor, MessageType, SentimentLevel
except ImportError:
    st.error("กรุณาใส่ extreme_dm_intelligence_extractor_2025.py ในโฟลเดอร์เดียวกัน")
    st.stop()

class DMIntelligenceDashboard:
    """🎯📊 แดชบอร์ดวิเคราะห์ DM ขั้นสูง"""
    
    def __init__(self, db_path="extreme_dm_intelligence_2025.db"):
        self.db_path = db_path
        self.extractor = ExtremeDMIntelligenceExtractor(db_path)
        
    def load_conversation_data(self) -> pd.DataFrame:
        """โหลดข้อมูลการสนทนาจากฐานข้อมูล"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT * FROM messages 
                ORDER BY timestamp DESC
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['hour'] = df['timestamp'].dt.hour
                df['day_of_week'] = df['timestamp'].dt.day_name()
                df['date'] = df['timestamp'].dt.date
                
            return df
        except Exception as e:
            st.error(f"ไม่สามารถโหลดข้อมูล: {e}")
            return pd.DataFrame()
    
    def load_conversation_stats(self) -> pd.DataFrame:
        """โหลดสถิติการสนทนา"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT * FROM conversation_stats ORDER BY analysis_date DESC"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"ไม่สามารถโหลดสถิติ: {e}")
            return pd.DataFrame()
    
    def render_main_dashboard(self):
        """แสดงแดshboard หลัก"""
        st.title("🎯📊 DM Intelligence Dashboard 2025")
        st.markdown("---")
        
        # Load data
        df = self.load_conversation_data()
        stats_df = self.load_conversation_stats()
        
        if df.empty:
            st.warning("ไม่มีข้อมูลการสนทนา - กรุณาดึงข้อมูล DM ก่อน")
            return
        
        # Sidebar controls
        st.sidebar.title("🎛️ ตัวควบคุม")
        
        # Date range filter
        min_date = df['date'].min()
        max_date = df['date'].max()
        date_range = st.sidebar.date_input(
            "เลือกช่วงวันที่",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Thread filter
        threads = df['thread_id'].unique()
        selected_threads = st.sidebar.multiselect(
            "เลือก Conversations",
            threads,
            default=threads[:5] if len(threads) > 5 else threads
        )
        
        # User filter
        users = df['sender_username'].unique()
        selected_users = st.sidebar.multiselect(
            "เลือกผู้ใช้",
            users,
            default=users
        )
        
        # Filter data
        filtered_df = df[
            (df['date'] >= date_range[0]) & 
            (df['date'] <= date_range[1]) &
            (df['thread_id'].isin(selected_threads)) &
            (df['sender_username'].isin(selected_users))
        ]
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📨 ข้อความทั้งหมด", len(filtered_df))
        
        with col2:
            unique_conversations = filtered_df['thread_id'].nunique()
            st.metric("💬 Conversations", unique_conversations)
        
        with col3:
            media_count = filtered_df['has_media'].sum()
            st.metric("🖼️ Media Messages", int(media_count))
        
        with col4:
            unique_users = filtered_df['sender_username'].nunique()
            st.metric("👥 ผู้ใช้", unique_users)
        
        # Charts
        self.render_activity_charts(filtered_df)
        self.render_sentiment_analysis(filtered_df)
        self.render_conversation_patterns(filtered_df)
        self.render_user_analysis(filtered_df)
    
    def render_activity_charts(self, df):
        """แสดงกราฟกิจกรรม"""
        st.subheader("📈 การวิเคราะห์กิจกรรม")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Messages by hour
            hourly_data = df.groupby('hour').size().reset_index(name='count')
            fig_hour = px.bar(
                hourly_data, 
                x='hour', 
                y='count',
                title="📊 ข้อความตามชั่วโมง",
                labels={'hour': 'ชั่วโมง', 'count': 'จำนวนข้อความ'}
            )
            fig_hour.update_layout(showlegend=False)
            st.plotly_chart(fig_hour, use_container_width=True)
        
        with col2:
            # Messages by day of week
            daily_data = df.groupby('day_of_week').size().reset_index(name='count')
            # Reorder days
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_data['day_of_week'] = pd.Categorical(daily_data['day_of_week'], categories=day_order, ordered=True)
            daily_data = daily_data.sort_values('day_of_week')
            
            fig_day = px.bar(
                daily_data, 
                x='day_of_week', 
                y='count',
                title="📊 ข้อความตามวันในสัปดาห์",
                labels={'day_of_week': 'วัน', 'count': 'จำนวนข้อความ'}
            )
            fig_day.update_layout(showlegend=False)
            st.plotly_chart(fig_day, use_container_width=True)
        
        # Timeline chart
        daily_timeline = df.groupby('date').size().reset_index(name='count')
        fig_timeline = px.line(
            daily_timeline,
            x='date',
            y='count',
            title="📈 Timeline ข้อความรายวัน"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    def render_sentiment_analysis(self, df):
        """แสดงการวิเคราะห์อารมณ์"""
        st.subheader("😊 การวิเคราะห์อารมณ์")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Overall sentiment distribution
            sentiment_counts = df['sentiment'].value_counts()
            fig_sentiment = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="🎭 การแจกแจงอารมณ์โดยรวม"
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col2:
            # Sentiment by user
            sentiment_user = df.groupby(['sender_username', 'sentiment']).size().unstack(fill_value=0)
            fig_sentiment_user = px.bar(
                sentiment_user.reset_index(),
                x='sender_username',
                y=sentiment_user.columns.tolist(),
                title="😊 อารมณ์ตามผู้ใช้",
                barmode='stack'
            )
            fig_sentiment_user.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_sentiment_user, use_container_width=True)
        
        # Sentiment over time
        sentiment_time = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        fig_sentiment_time = px.area(
            sentiment_time.reset_index(),
            x='date',
            y=sentiment_time.columns.tolist(),
            title="📈 แนวโน้มอารมณ์ตามเวลา"
        )
        st.plotly_chart(fig_sentiment_time, use_container_width=True)
    
    def render_conversation_patterns(self, df):
        """แสดงรูปแบบการสนทนา"""
        st.subheader("🔍 รูปแบบการสนทนา")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Message types distribution
            type_counts = df['message_type'].value_counts()
            fig_types = px.bar(
                x=type_counts.values,
                y=type_counts.index,
                orientation='h',
                title="📱 ประเภทข้อความ"
            )
            st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            # Message length distribution
            df['content_length'] = df['content'].str.len()
            fig_length = px.histogram(
                df,
                x='content_length',
                title="📏 การแจกแจงความยาวข้อความ",
                nbins=50
            )
            st.plotly_chart(fig_length, use_container_width=True)
        
        # Conversation activity heatmap
        df['hour'] = df['timestamp'].dt.hour
        df['day_num'] = df['timestamp'].dt.dayofweek
        day_names = ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัส', 'ศุกร์', 'เสาร์', 'อาทิตย์']
        
        heatmap_data = df.groupby(['day_num', 'hour']).size().unstack(fill_value=0)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=list(range(24)),
            y=[day_names[i] for i in heatmap_data.index],
            colorscale='Blues',
            hoverongaps=False
        ))
        
        fig_heatmap.update_layout(
            title="🔥 Heatmap กิจกรรมการสนทนา",
            xaxis_title="ชั่วโมง",
            yaxis_title="วัน"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    def render_user_analysis(self, df):
        """แสดงการวิเคราะห์ผู้ใช้"""
        st.subheader("👥 การวิเคราะห์ผู้ใช้")
        
        # User statistics
        user_stats = df.groupby('sender_username').agg({
            'id': 'count',
            'content': lambda x: x.str.len().mean(),
            'has_media': 'sum',
            'confidence_score': 'mean'
        }).round(2)
        
        user_stats.columns = ['จำนวนข้อความ', 'ความยาวเฉลี่ย', 'Media Messages', 'คะแนนความเชื่อมั่น']
        user_stats = user_stats.sort_values('จำนวนข้อความ', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("📊 สถิติผู้ใช้")
            st.dataframe(user_stats)
        
        with col2:
            # Top users by message count
            fig_users = px.bar(
                x=user_stats.index[:10],
                y=user_stats['จำนวนข้อความ'][:10],
                title="🏆 ผู้ใช้ที่ส่งข้อความมากที่สุด"
            )
            fig_users.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_users, use_container_width=True)
        
        # User interaction network (if multiple users per thread)
        st.subheader("🕸️ เครือข่ายการปฏิสัมพันธ์")
        
        # Create interaction matrix
        thread_users = df.groupby('thread_id')['sender_username'].apply(list).reset_index()
        interactions = {}
        
        for _, row in thread_users.iterrows():
            users = list(set(row['sender_username']))
            if len(users) > 1:
                for i, user1 in enumerate(users):
                    for user2 in users[i+1:]:
                        pair = tuple(sorted([user1, user2]))
                        interactions[pair] = interactions.get(pair, 0) + 1
        
        if interactions:
            interaction_df = pd.DataFrame([
                {'User 1': pair[0], 'User 2': pair[1], 'Interactions': count}
                for pair, count in interactions.items()
            ]).sort_values('Interactions', ascending=False)
            
            st.write("Top 10 การปฏิสัมพันธ์")
            st.dataframe(interaction_df.head(10))
    
    def render_real_time_monitor(self):
        """แสดงการติดตามแบบ real-time"""
        st.subheader("🔄 การติดตามแบบ Real-time")
        
        if 'monitoring_active' not in st.session_state:
            st.session_state.monitoring_active = False
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 เริ่มการติดตาม"):
                st.session_state.monitoring_active = True
                st.success("เริ่มการติดตาม real-time")
        
        with col2:
            if st.button("⏹️ หยุดการติดตาม"):
                st.session_state.monitoring_active = False
                st.info("หยุดการติดตาม")
        
        if st.session_state.monitoring_active:
            # Placeholder for real-time data
            st.info("🔄 กำลังติดตาม... (Feature นี้ต้องใช้ server backend)")
            
            # Show recent messages
            df = self.load_conversation_data()
            if not df.empty:
                recent_messages = df.head(10)
                st.write("📨 ข้อความล่าสุด")
                st.dataframe(recent_messages[['timestamp', 'sender_username', 'content', 'sentiment']])
    
    def render_data_export(self):
        """แสดงการส่งออกข้อมูล"""
        st.subheader("📤 ส่งออกข้อมูล")
        
        df = self.load_conversation_data()
        if df.empty:
            st.warning("ไม่มีข้อมูลให้ส่งออก")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 ส่งออก Excel"):
                output_path = f"dm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df.to_excel(output_path, index=False)
                st.success(f"ส่งออกเป็น {output_path}")
        
        with col2:
            if st.button("📄 ส่งออก CSV"):
                output_path = f"dm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(output_path, index=False)
                st.success(f"ส่งออกเป็น {output_path}")
        
        with col3:
            if st.button("📋 ส่งออก JSON"):
                output_path = f"dm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                df.to_json(output_path, orient='records', indent=2)
                st.success(f"ส่งออกเป็น {output_path}")

def main():
    """ฟังก์ชันหลักของแดshboard"""
    st.set_page_config(
        page_title="DM Intelligence Dashboard 2025",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    dashboard = DMIntelligenceDashboard()
    
    # Navigation
    page = st.sidebar.selectbox(
        "🧭 เลือกหน้า",
        ["📊 Dashboard หลัก", "🔄 Real-time Monitor", "📤 ส่งออกข้อมูล"]
    )
    
    if page == "📊 Dashboard หลัก":
        dashboard.render_main_dashboard()
    elif page == "🔄 Real-time Monitor":
        dashboard.render_real_time_monitor()
    elif page == "📤 ส่งออกข้อมูล":
        dashboard.render_data_export()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("🧠💬 **DM Intelligence Dashboard 2025**")
    st.sidebar.markdown("Created by น้องจิน (chin4d0ll) ♥️")

if __name__ == "__main__":
    main()
