import glfw

def create(altura, largura):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(largura, altura, "Trabalho 1", None, None)
    glfw.make_context_current(window)
    return window