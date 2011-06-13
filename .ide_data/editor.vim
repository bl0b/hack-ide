" ~/bl0b_dev/hack-ide/.ide_data/editor.vim: Vim session script.
" Created by ~/.vim/autoload/xolox/session.vim on 13 juin 2011 at 11:51:13.
" Open this file in Vim and run :source % to restore your session.

set guioptions=batgirl
silent! set guifont=
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if !exists('g:colors_name') || g:colors_name != 'torte' | colorscheme torte | endif
set background=dark
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/bl0b_dev/hack-ide
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +49 py/main.py
badd +164 py/task.py
badd +19 py/base.py
badd +7 py/layout.py
badd +1 py/hackide.py
badd +1 py/rc_file.py
badd +17 py/sandbox.py
badd +1 py/tmux.py
silent! argdel *
set lines=69 columns=130
edit py/base.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd w
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 14 + 65) / 130)
exe '2resize ' . ((&lines * 22 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 70 + 65) / 130)
exe '3resize ' . ((&lines * 22 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 44 + 65) / 130)
exe '4resize ' . ((&lines * 22 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 98 + 65) / 130)
exe '5resize ' . ((&lines * 21 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 98 + 65) / 130)
exe '6resize ' . ((&lines * 44 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 16 + 65) / 130)
argglobal
enew
file NERD_tree_1
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
wincmd w
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 7 - ((6 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 0
wincmd w
argglobal
edit py/task.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 116 - ((11 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
116
normal! 019l
wincmd w
argglobal
edit py/main.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit py/layout.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 277 - ((14 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
277
normal! 0
wincmd w
argglobal
edit py/tmux.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 6 - ((2 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
6
normal! 064l
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 14 + 65) / 130)
exe '2resize ' . ((&lines * 22 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 70 + 65) / 130)
exe '3resize ' . ((&lines * 22 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 44 + 65) / 130)
exe '4resize ' . ((&lines * 22 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 98 + 65) / 130)
exe '5resize ' . ((&lines * 21 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 98 + 65) / 130)
exe '6resize ' . ((&lines * 44 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 16 + 65) / 130)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
tabnext 1
1wincmd w
bwipeout
NERDTree ~/bl0b_dev/hack-ide
1resize 67|vert 1resize 14|2resize 22|vert 2resize 70|3resize 22|vert 3resize 44|4resize 22|vert 4resize 94|5resize 21|vert 5resize 94|6resize 44|vert 6resize 20|
tabnext 1
4wincmd w

" vim: ft=vim ro nowrap smc=128
