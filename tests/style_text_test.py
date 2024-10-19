from writtenbookeditor.minimessage.style import StyleText, Style


def test_style_text():
    style = Style()
    style.color_mode = "rainbow"
    style.rainbow_phase = 2
    st = StyleText("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||", style)
    result = st.to_components()
    result = [i.to_dict() for i in result]
    print(result)
