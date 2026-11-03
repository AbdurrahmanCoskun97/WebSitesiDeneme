import streamlit as st

st.set_page_config(page_title="Hesap Makinesi", page_icon="🧮", layout="centered")

st.title("🧮 Hesap Makinesi")

# 1. State Başlatma
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "history" not in st.session_state:
    st.session_state.history = []

# 2. Callback Fonksiyonları (Sayfa çizilmeden önce çalışırlar)
def append_char(char):
    st.session_state.expression += str(char)

def clear_all():
    st.session_state.expression = ""

def delete_last():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    expr = st.session_state.expression
    if not expr:
        return

    eval_expr = expr.replace("×", "*").replace("÷", "/")

    try:
        # % karakteri de dahil izin verilen karakter seti
        allowed_chars = set("0123456789+-*/.%() ")
        if not set(eval_expr).issubset(allowed_chars):
            raise ValueError("Geçersiz karakter")

        result = eval(eval_expr, {"__builtins__": None}, {})

        # 5.0 gibi değerleri 5 olarak formatla
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 6)

        st.session_state.history.append(f"{expr} = {result}")
        st.session_state.expression = str(result)
    except ZeroDivisionError:
        st.session_state.expression = "Sıfıra bölünemez"
    except Exception:
        st.session_state.expression = "Hata"

# 3. Ekran (Display)
display_text = st.session_state.expression if st.session_state.expression else "0"
st.markdown(
    f"""
    <div style="
        background-color: #1e1e1e;
        color: #00ff66;
        font-family: monospace;
        font-size: 2rem;
        padding: 12px 18px;
        text-align: right;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 15px;
        overflow-x: auto;
    ">
        {display_text}
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Tuş Takımı (Tümü on_click callback ile bağlı)
grid = [
    [("C", clear_all, None), ("⌫", delete_last, None), ("%", append_char, "%"), ("÷", append_char, "÷")],
    [("7", append_char, "7"), ("8", append_char, "8"), ("9", append_char, "9"), ("×", append_char, "×")],
    [("4", append_char, "4"), ("5", append_char, "5"), ("6", append_char, "6"), ("-", append_char, "-")],
    [("1", append_char, "1"), ("2", append_char, "2"), ("3", append_char, "3"), ("+", append_char, "+")],
    [("0", append_char, "0"), (".", append_char, "."), ("=", calculate, None), ("x²", append_char, "**2")]
]

for row in grid:
    cols = st.columns(4)
    for col, (label, func, arg) in zip(cols, row):
        with col:
            is_action = label in ["=", "C", "⌫"]
            if arg is not None:
                st.button(
                    label,
                    on_click=func,
                    args=(arg,),
                    use_container_width=True,
                    type="primary" if label == "=" else "secondary"
                )
            else:
                st.button(
                    label,
                    on_click=func,
                    use_container_width=True,
                    type="primary" if label == "=" else "secondary"
                )

# 5. İşlem Geçmişi
if st.session_state.history:
    with st.expander("🕒 İşlem Geçmişi", expanded=False):
        for item in reversed(st.session_state.history[-8:]):
            st.code(item, language="text")
        st.button("Geçmişi Temizle", on_click=lambda: st.session_state.history.clear())