import streamlit as st

# ==========================================
# 1. DATA MATERIAL (Sesuai Spreadsheet)
# ==========================================

# Biaya Ascension Karakter (Level 40 - 90)
# Format: {Level: {'mora': x, 'common_t1': x, 'specialty': x, 'gem_t2': x, 'gem_t3': x, 'gem_t4': x, 'gem_t5': x, 'boss': x}}
ASCENSION_COSTS = {
    40: {'mora': 20000, 'common_t1': 3, 'specialty': 3, 'gem_t2': 1, 'gem_t3': 0, 'gem_t4': 0, 'gem_t5': 0, 'boss': 0},
    50: {'mora': 40000, 'common_t1': 15, 'specialty': 10, 'gem_t2': 0, 'gem_t3': 3, 'gem_t4': 0, 'gem_t5': 0, 'boss': 2},
    60: {'mora': 60000, 'common_t2': 12, 'specialty': 20, 'gem_t2': 0, 'gem_t3': 6, 'gem_t4': 0, 'gem_t5': 0, 'boss': 4},
    70: {'mora': 80000, 'common_t2': 18, 'specialty': 30, 'gem_t2': 0, 'gem_t3': 0, 'gem_t4': 3, 'gem_t5': 0, 'boss': 8},
    80: {'mora': 100000, 'common_t3': 12, 'specialty': 45, 'gem_t2': 0, 'gem_t3': 0, 'gem_t4': 6, 'gem_t5': 0, 'boss': 12},
    90: {'mora': 120000, 'common_t3': 24, 'specialty': 60, 'gem_t2': 0, 'gem_t3': 0, 'gem_t4': 0, 'gem_t5': 6, 'boss': 20}
}

# Biaya Talent (Level 2 - 10)
# Format: {Level: {'mora': x, 'book_t2': x, 'book_t3': x, 'book_t4': x, 'common_t1': x, 'common_t2': x, 'common_t3': x, 'boss_weekly': x, 'crown': x}}
TALENT_COSTS = {
    2: {'mora': 12500, 'book_t2': 3, 'book_t3': 0, 'book_t4': 0, 'common_t1': 6, 'common_t2': 0, 'common_t3': 0, 'boss_weekly': 0, 'crown': 0},
    3: {'mora': 17500, 'book_t2': 0, 'book_t3': 2, 'book_t4': 0, 'common_t1': 0, 'common_t2': 3, 'common_t3': 0, 'boss_weekly': 0, 'crown': 0},
    4: {'mora': 25000, 'book_t2': 0, 'book_t3': 4, 'book_t4': 0, 'common_t1': 0, 'common_t2': 4, 'common_t3': 0, 'boss_weekly': 0, 'crown': 0},
    5: {'mora': 30000, 'book_t2': 0, 'book_t3': 9, 'book_t4': 0, 'common_t1': 0, 'common_t2': 6, 'common_t3': 0, 'boss_weekly': 0, 'crown': 0},
    6: {'mora': 35000, 'book_t2': 0, 'book_t3': 9, 'book_t4': 0, 'common_t1': 0, 'common_t2': 9, 'common_t3': 0, 'boss_weekly': 0, 'crown': 0},
    7: {'mora': 120000, 'book_t2': 0, 'book_t3': 0, 'book_t4': 4, 'common_t1': 0, 'common_t2': 0, 'common_t3': 4, 'boss_weekly': 1, 'crown': 0},
    8: {'mora': 260000, 'book_t2': 0, 'book_t3': 0, 'book_t4': 6, 'common_t1': 0, 'common_t2': 0, 'common_t3': 6, 'boss_weekly': 1, 'crown': 0},
    9: {'mora': 450000, 'book_t2': 0, 'book_t3': 0, 'book_t4': 12, 'common_t1': 0, 'common_t2': 0, 'common_t3': 9, 'boss_weekly': 2, 'crown': 0},
    10: {'mora': 700000, 'book_t2': 0, 'book_t3': 0, 'book_t4': 16, 'common_t1': 0, 'common_t2': 0, 'common_t3': 12, 'boss_weekly': 2, 'crown': 1}
}

# Total EXP dan Mora untuk Level 1 - 90 (Hero's Wit)
CHAR_EXP_TOTAL = {
    'mora_level': 1673400, # Mora untuk naik level (bukan ascension)
    'exp': 8362500         # Total EXP (1 Hero's Wit = 20,000 EXP)
}

# ==========================================
# 2. FUNGSI PERHITUNGAN
# ==========================================

def hitung_talent(target_level):
    total = {'mora': 0, 'book_t2': 0, 'book_t3': 0, 'book_t4': 0, 'common_t1': 0, 'common_t2': 0, 'common_t3': 0, 'boss_weekly': 0, 'crown': 0}
    if target_level <= 1:
        return total
    for lv in range(2, target_level + 1):
        for key in total.keys():
            total[key] += TALENT_COSTS[lv].get(key, 0)
    return total

def hitung_karakter(target_level):
    total = {'mora_ascension': 0, 'common_t1': 0, 'common_t2': 0, 'common_t3': 0, 'specialty': 0, 'gem_t2': 0, 'gem_t3': 0, 'gem_t4': 0, 'gem_t5': 0, 'boss': 0}
    if target_level >= 40:
        for lv, cost in ASCENSION_COSTS.items():
            if target_level >= lv:
                for key in total.keys():
                    if key in cost:
                        total[key] += cost[key]
    return total

def hitung_kurang(butuh, punya):
    return max(0, butuh - punya)

def konversi_ke_t1(jumlah, tier):
    """Konversi material ke Tier 1 (bintang 1). Rumus: 3^(tier-1)"""
    if jumlah <= 0: return 0
    return jumlah * (3 ** (tier - 1))

# ==========================================
# 3. TAMPILAN WEB (STREAMLIT UI)
# ==========================================

st.set_page_config(page_title="Genshin Material Calculator", page_icon="🧮", layout="wide")

# CSS Kustom untuk Card Material
def render_material_card(icon, nama, butuh, punya, warna_bg, warna_teks="#1a1a1a"):
    kurang = hitung_kurang(butuh, punya)
    
    if kurang == 0:
        status_color = "#4caf50" # Hijau
        teks_status = "✅ Cukup"
        teks_angka = "0"
    else:
        status_color = "#f44336" # Merah
        teks_status = "❌ Kurang"
        teks_angka = f"{kurang:,}"
        
    html = f"""
    <div style="background-color: {warna_bg}; padding: 12px; border-radius: 8px; 
                color: {warna_teks}; margin-bottom: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                border-left: 5px solid {status_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: bold; font-size: 15px;">{icon} {nama}</div>
            <div style="font-size: 12px; background: rgba(0,0,0,0.1); padding: 2px 8px; border-radius: 10px;">
                Butuh: {butuh:,} | Punya: {punya:,}
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
            <div style="font-size: 14px; font-weight: bold; color: {status_color};">{teks_status}</div>
            <div style="font-size: 20px; font-weight: bold;">{teks_angka}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- SIDEBAR: INPUT TARGET & INVENTORY ---
with st.sidebar:
    st.header("🎯 Target Karakter")
    char_level = st.number_input("Level Karakter (1-90)", min_value=1, max_value=90, value=90, step=1)
    
    st.markdown("**Level Talenta:**")
    talent_na = st.slider("Normal Attack", 1, 10, 1)
    talent_skill = st.slider("Elemental Skill", 1, 10, 1)
    talent_burst = st.slider("Elemental Burst", 1, 10, 1)
    
    st.divider()
    st.header("📦 Material yang Dimiliki")
    st.markdown("Masukkan jumlah material di inventory kamu.")
    
    with st.expander("💰 Mora & EXP", expanded=False):
        inv_mora = st.number_input("Mora", min_value=0, value=0, step=10000)
        inv_hero_wit = st.number_input("Hero's Wit", min_value=0, value=0, step=10)
        
    with st.expander("🐾 Monster Drops (Common)", expanded=False):
        inv_common_t1 = st.number_input("Common Tier 1 (Bintang 1)", min_value=0, value=0)
        inv_common_t2 = st.number_input("Common Tier 2 (Bintang 2)", min_value=0, value=0)
        inv_common_t3 = st.number_input("Common Tier 3 (Bintang 3)", min_value=0, value=0)
        
    with st.expander("🐻 Boss & Specialty", expanded=False):
        inv_specialty = st.number_input("Specialty (Local Specialty)", min_value=0, value=0)
        inv_boss = st.number_input("Boss Material (Ascension)", min_value=0, value=0)
        inv_boss_weekly = st.number_input("Weekly Boss Material", min_value=0, value=0)
        
    with st.expander("💎 Gem Ascension", expanded=False):
        inv_gem_t2 = st.number_input("Gem Tier 2 (Bintang 2)", min_value=0, value=0)
        inv_gem_t3 = st.number_input("Gem Tier 3 (Bintang 3)", min_value=0, value=0)
        inv_gem_t4 = st.number_input("Gem Tier 4 (Bintang 4)", min_value=0, value=0)
        inv_gem_t5 = st.number_input("Gem Tier 5 (Bintang 5)", min_value=0, value=0)
        
    with st.expander("📖 Buku Talent & Crown", expanded=False):
        inv_book_t2 = st.number_input("Buku Talent Tier 2 (Bintang 2)", min_value=0, value=0)
        inv_book_t3 = st.number_input("Buku Talent Tier 3 (Bintang 3)", min_value=0, value=0)
        inv_book_t4 = st.number_input("Buku Talent Tier 4 (Bintang 4)", min_value=0, value=0)
        inv_crown = st.number_input("Crown of Insight", min_value=0, value=0)

# --- PROSES HITUNG ---
na_cost = hitung_talent(talent_na)
skill_cost = hitung_talent(talent_skill)
burst_cost = hitung_talent(talent_burst)

total_talent = {}
for key in na_cost.keys():
    total_talent[key] = na_cost[key] + skill_cost[key] + burst_cost[key]

char_cost = hitung_karakter(char_level)
hero_wit_butuh = int(CHAR_EXP_TOTAL['exp'] / 20000) if char_level >= 90 else 0

# Gabungan Total Kebutuhan
total_mora_butuh = char_cost['mora_ascension'] + CHAR_EXP_TOTAL['mora_level'] + total_talent['mora']
total_common_t1_butuh = char_cost['common_t1'] + total_talent['common_t1']
total_common_t2_butuh = char_cost['common_t2'] + total_talent['common_t2']
total_common_t3_butuh = char_cost['common_t3'] + total_talent['common_t3']

# --- OUTPUT SECTION ---
st.title("🧮 Genshin Material Calculator")
st.markdown("Hitung total material dan sisa kekurangan untuk menaikkan level karakter dan talenta.")

if char_level < 90:
    st.warning("⚠️ Catatan: Perhitungan EXP dan Mora untuk naik level (1-90) hanya akurat jika kamu memilih Level 90. Untuk level di bawah 90, angka EXP mungkin sedikit berbeda karena kurva EXP per level.")

# Membuat Tabs agar rapi
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Mora & EXP", "🐾 Monster & Boss", "📖 Buku Talent", "💎 Gem & Specialty", "🔄 Konversi Tier 1"])

# --- TAB 1: MORA & EXP ---
with tab1:
    st.subheader("Mora & EXP")
    col1, col2 = st.columns(2)
    with col1:
        render_material_card("🪙", "Total Mora (Ascension + Talent + Level)", total_mora_butuh, inv_mora, "#FFFF00")
    with col2:
        render_material_card("📘", "Hero's Wit (EXP Buku)", hero_wit_butuh, inv_hero_wit, "#a67cc2", "#ffffff")

# --- TAB 2: MONSTER & BOSS ---
with tab2:
    st.subheader("Material Monster & Boss")
    st.markdown("Material ini didapat dari mengalahkan musuh.")
    
    col1, col2 = st.columns(2)
    with col1:
        render_material_card("🐾", "Common Monster Drop T1 (Bintang 1)", total_common_t1_butuh, inv_common_t1, "#A9A9A9")
        render_material_card("🐾", "Common Monster Drop T2 (Bintang 2)", total_common_t2_butuh, inv_common_t2, "#9EEF88")
        render_material_card("🐾", "Common Monster Drop T3 (Bintang 3)", total_common_t3_butuh, inv_common_t3, "#558AD5")
    with col2:
        render_material_card("🐻", "Boss Material (Ascension)", char_cost['boss'], inv_boss, "#983298", "#ffffff")
        render_material_card("🐉", "Weekly Boss Material", total_talent['boss_weekly'], inv_boss_weekly, "#FFA500")

# --- TAB 3: BUKU TALENT ---
with tab3:
    st.subheader("Buku Talent & Crown")
    st.markdown("Material ini didapat dari Domain Talent (Senin/Kamis, dll).")
    
    col1, col2 = st.columns(2)
    with col1:
        render_material_card("📖", "Buku Talent T2 (Bintang 2)", total_talent['book_t2'], inv_book_t2, "#9EEF88")
        render_material_card("📖", "Buku Talent T3 (Bintang 3)", total_talent['book_t3'], inv_book_t3, "#558AD5")
        render_material_card("📖", "Buku Talent T4 (Bintang 4)", total_talent['book_t4'], inv_book_t4, "#983298")
    with col2:
        render_material_card("👑", "Crown of Insight", total_talent['crown'], inv_crown, "#FFA500")

# --- TAB 4: GEM & SPECIALTY ---
with tab4:
    st.subheader("Gem & Specialty")
    st.markdown("Material ini didapat dari Boss Dunia dan alam terbuka.")
    
    col1, col2 = st.columns(2)
    with col1:
        render_material_card("🌸", "Local Specialty", char_cost['specialty'], inv_specialty, "#A9A9A9")
    with col2:
        render_material_card("💎", "Gem T2 (Bintang 2)", char_cost['gem_t2'], inv_gem_t2, "#9EEF88")
        render_material_card("💎", "Gem T3 (Bintang 3)", char_cost['gem_t3'], inv_gem_t3, "#558AD5")
        render_material_card("💎", "Gem T4 (Bintang 4)", char_cost['gem_t4'], inv_gem_t4, "#983298")
        render_material_card("💎", "Gem T5 (Bintang 5)", char_cost['gem_t5'], inv_gem_t5, "#FFA500")

# --- TAB 5: KONVERSI TIER 1 ---
with tab5:
    st.subheader("🔄 Hitungan Tambahan (Konversi ke Tier Terendah)")
    st.markdown("""
    Sesuai catatan pada spreadsheet:
    *   **Monster Drops (Common):** Dimulai dari Bintang 1.
        *   1 (Bintang 5) = 81 (Bintang 1)
        *   1 (Bintang 4) = 27 (Bintang 1)
        *   1 (Bintang 3) = 9 (Bintang 1)
        *   1 (Bintang 2) = 3 (Bintang 1)
    *   **Buku Talent:** Dimulai dari Bintang 2 (Tier 2).
        *   1 (Bintang 5) = 27 (Bintang 2)
        *   1 (Bintang 4) = 9 (Bintang 2)
        *   1 (Bintang 3) = 3 (Bintang 2)
    """)
    
    st.markdown("---")
    
    # --- HITUNG TOTAL KEBUTUHAN ---
    # Monster dikonversi ke Tier 1 (Bintang 1)
    total_monster_t1_butuh = total_common_t1_butuh + (total_common_t2_butuh * 3) + (total_common_t3_butuh * 9)
    # Buku Talent dikonversi ke Tier 2 (Bintang 2)
    total_buku_t2_butuh = total_talent['book_t2'] + (total_talent['book_t3'] * 3) + (total_talent['book_t4'] * 9)
    
    # --- HITUNG TOTAL DIMILIKI ---
    total_monster_t1_dimiliki = inv_common_t1 + (inv_common_t2 * 3) + (inv_common_t3 * 9)
    total_buku_t2_dimiliki = inv_book_t2 + (inv_book_t3 * 3) + (inv_book_t4 * 9)
    
    # --- HITUNG SISA YANG DICARI ---
    sisa_monster_t1 = max(0, total_monster_t1_butuh - total_monster_t1_dimiliki)
    sisa_buku_t2 = max(0, total_buku_t2_butuh - total_buku_t2_dimiliki)

    # --- TAMPILKAN MONSTER ---
    st.markdown("### 🐾 Monster (Common Drops)")
    st.caption("Konversi ke Tier 1 (Bintang 1)")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""<div style="background-color: #A9A9A9; padding: 15px; border-radius: 8px; color: #1a1a1a; text-align: center;">
            <h4 style="margin: 0;">Total Kebutuhan (T1)</h4>
            <h2 style="margin: 5px 0; font-size: 28px;">{total_monster_t1_butuh:,}</h2>
        </div>""", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""<div style="background-color: #D3D3D3; padding: 15px; border-radius: 8px; color: #1a1a1a; text-align: center;">
            <h4 style="margin: 0;">Total Dimiliki (T1)</h4>
            <h2 style="margin: 5px 0; font-size: 28px;">{total_monster_t1_dimiliki:,}</h2>
        </div>""", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""<div style="background-color: #ffcccc; padding: 15px; border-radius: 8px; color: #1a1a1a; text-align: center; border: 2px solid #f44336;">
            <h4 style="margin: 0;">Sisa yang Dicari (T1)</h4>
            <h2 style="margin: 5px 0; font-size: 28px; color: #b71c1c;">{sisa_monster_t1:,}</h2>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TAMPILKAN BUKU TALENT ---
    st.markdown("### 📖 Buku Talent")
    st.caption("Konversi ke Tier 2 (Bintang 2) - Tier terendah buku talent")
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown(f"""<div style="background-color: #00FF00; padding: 15px; border-radius: 8px; color: #1a1a1a; text-align: center;">
            <h4 style="margin: 0;">Total Kebutuhan (T2)</h4>
            <h2 style="margin: 5px 0; font-size: 28px;">{total_buku_t2_butuh:,}</h2>
        </div>""", unsafe_allow_html=True)
    with col_b2:
        st.markdown(f"""<div style="background-color: #ccffcc; padding: 15px; border-radius: 8px; color: #1a1a1a; text-align: center;">
            <h4 style="margin: 0;">Total Dimiliki (T2)</h4>
            <h2 style="margin: 5px 0; font-size: 28px;">{total_buku_t2_dimiliki:,}</h2>
        </div>""", unsafe_allow_html=True)
    with col_b3:
        st.markdown(f"""<div style="background-color: #ffcccc; padding: 15px; border-radius: 8px; color: #1a1a1a; text-align: center; border: 2px solid #f44336;">
            <h4 style="margin: 0;">Sisa yang Dicari (T2)</h4>
            <h2 style="margin: 5px 0; font-size: 28px; color: #b71c1c;">{sisa_buku_t2:,}</h2>
        </div>""", unsafe_allow_html=True)

    st.caption("*Catatan: Total Dimiliki Buku Talent dikonversi dari inventory kamu (1 T3 = 3 T2, 1 T4 = 9 T2).*")