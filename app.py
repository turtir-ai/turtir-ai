import streamlit as st
from scraper import setup_chrome_driver, perform_manual_login, scrape_jobs_with_driver
from analyzer import analyze_job_description
from database import init_db, add_project, get_all_projects, update_status, get_project_stats
import time

# Page configuration
st.set_page_config(
    page_title="Upwork Proje Asistanı",
    page_icon="🔍",
    layout="wide"
)

def main():
    """Main application function."""
    # Initialize database
    init_db()
    
    # Header
    st.title("🔍 Kişiselleştirilmiş Upwork Proje Asistanı")
    st.markdown("AI destekli proje analizi ile size en uygun Upwork projelerini bulun!")
    st.divider()
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        search_query = st.text_input("Arama Terimi", value="web development")
        max_pages = st.slider("Maksimum Sayfa", 1, 5, 2)
        
        st.divider()
        
        st.header("📊 İstatistikler")
        stats = get_project_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Toplam", sum(stats.values()))
            st.metric("Beklemede", stats['Beklemede'])
        with col2:
            st.metric("Başvuruldu", stats['Başvuruldu'])
            st.metric("Kazanıldı", stats['Kazanıldı'])
    
    # Main action button
    col1, col2 = st.columns([2, 2])
    with col1:
        if st.button("🔍 Yeni Projeleri Tara ve Analiz Et", type="primary", use_container_width=True):
            # Initialize session state for driver management
            if 'scraping_active' not in st.session_state:
                st.session_state.scraping_active = False
            
            if not st.session_state.scraping_active:
                st.session_state.scraping_active = True
                
                # Create containers for status updates
                status_container = st.container()
                progress_container = st.container()
                
                with status_container:
                    st.info("🚀 Starting browser and navigating to Upwork...")
                
                driver = None
                try:
                    # Setup Chrome driver
                    with status_container:
                        st.info("🔧 Setting up Chrome browser...")
                    
                    driver = setup_chrome_driver()
                    
                    with status_container:
                        st.warning("⏳ Please complete manual login in the browser window. You have 60 seconds.")
                        st.markdown("**Steps:**")
                        st.markdown("1. Login to Upwork in the opened browser")
                        st.markdown("2. Complete 2FA if required")
                        st.markdown("3. Wait for automatic continuation")
                    
                    # Perform manual login
                    perform_manual_login(driver)
                    
                    with status_container:
                        st.success("✅ Login completed! Starting to scrape jobs...")
                    
                    # Scrape jobs
                    jobs = scrape_jobs_with_driver(driver, search_query, max_pages)
                    
                    if jobs:
                        with status_container:
                            st.success(f"🎉 Found {len(jobs)} jobs! Starting AI analysis...")
                        
                        with progress_container:
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                        
                        added_count = 0
                        
                        for i, job in enumerate(jobs):
                            # Update progress
                            progress = (i + 1) / len(jobs)
                            progress_bar.progress(progress)
                            status_text.text(f"Analyzing job {i+1}/{len(jobs)}: {job['title'][:50]}...")
                            
                            # Analyze job
                            analysis = analyze_job_description(job['description'])
                            
                            # Prepare project data
                            project_data = {
                                'title': job['title'],
                                'link': job['link'],
                                'description': job['description'],
                                'suitability_score': analysis['uygunluk_skoru'],
                                'analysis_summary': analysis['analiz_ozeti'],
                                'technologies': analysis['gereken_teknolojiler']
                            }
                            
                            # Add to database
                            if add_project(project_data):
                                added_count += 1
                        
                        with status_container:
                            st.success(f"🎊 Process completed! {added_count} new projects added to database.")
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        status_text.empty()
                        
                    else:
                        with status_container:
                            st.warning("⚠️ No jobs found. Try different search terms.")
                
                except Exception as e:
                    st.error(f"❌ Error occurred: {str(e)}")
                
                finally:
                    # Always close the driver
                    if driver:
                        try:
                            driver.quit()
                            with status_container:
                                st.info("🔒 Browser closed safely.")
                        except:
                            pass
                    
                    # Reset session state
                    st.session_state.scraping_active = False
                    
                    # Auto-refresh to show new results
                    time.sleep(2)
                    st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Results", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Display projects
    st.header("📋 Bulunan Projeler")
    
    projects = get_all_projects()
    
    if not projects:
        st.info("Henüz proje yok. Yukarıdaki butona tıklayarak taramaya başlayın!")
        return
    
    # Filter by score
    min_score = st.slider("Minimum Uygunluk Skoru", 1, 10, 1)
    filtered_projects = [p for p in projects if p['suitability_score'] >= min_score]
    
    st.write(f"**{len(filtered_projects)}** proje gösteriliyor")
    
    # Display projects
    for project in filtered_projects:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Project title and link
                st.markdown(f"### [{project['title']}]({project['link']})")
                
                # Score with color
                score = project['suitability_score']
                if score >= 8:
                    st.markdown(f"**Uygunluk:** 🟢 {score}/10")
                elif score >= 6:
                    st.markdown(f"**Uygunluk:** 🟡 {score}/10")
                else:
                    st.markdown(f"**Uygunluk:** 🔴 {score}/10")
                
                # Analysis summary
                st.markdown(f"**Analiz:** {project['analysis_summary']}")
                
                # Technologies
                if project['technologies']:
                    tech_str = " • ".join([f"`{tech}`" for tech in project['technologies']])
                    st.markdown(f"**Teknolojiler:** {tech_str}")
            
            with col2:
                # Status selector
                status_options = ['Beklemede', 'Başvuruldu', 'Kazanıldı', 'Kaybedildi']
                current_status = project['application_status']
                
                new_status = st.selectbox(
                    "Durum",
                    status_options,
                    index=status_options.index(current_status),
                    key=f"status_{project['id']}"
                )
                
                if new_status != current_status:
                    if update_status(project['id'], new_status):
                        st.success("Güncellendi!")
                        st.rerun()
            
            with col3:
                # Details expander
                if st.button("Detaylar", key=f"details_{project['id']}"):
                    st.text_area("Açıklama", project['description'], height=150, disabled=True, key=f"desc_{project['id']}")
            
            st.divider()

if __name__ == "__main__":
    main()