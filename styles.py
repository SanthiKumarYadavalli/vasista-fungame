CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Prata&display=swap');

body{
    text-align: center
} 

div[data-testid="stImage"] img {
    position: absolute;
    left: calc(50% - 295px);
    border-radius: 25px;
}

section[data-testid="stSidebar"] img {
    position: static;
}

h2 span {
    display: none !important;
}

.block-container * {
    font-family: 'Comic Neue', "Source Sans Pro", sans-serif;
    font-weight: 400;
}

</style>
"""