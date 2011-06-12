" ~/bl0b_dev/hack-ide/.ide_data/editor.vim: Vim session script.
" Created by ~/.vim/autoload/xolox/session.vim on 12 juin 2011 at 17:31:02.
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
badd +1 py/main.py
badd +164 py/task.py
badd +19 py/base.py
badd +7 py/layout.py
badd +1 py/hackide.py
badd +1 py/rc_file.py
badd +17 py/sandbox.py
badd +0 py/tmux.py
silent! argdel *
set lines=57 columns=119
edit py/main.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 14 + 59) / 119)
exe '2resize ' . ((&lines * 27 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 104 + 59) / 119)
exe '3resize ' . ((&lines * 27 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 104 + 59) / 119)
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
let s:l = 31 - ((0 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 08l
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
let s:l = 23 - ((12 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
23
normal! 032l
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 14 + 59) / 119)
exe '2resize ' . ((&lines * 27 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 104 + 59) / 119)
exe '3resize ' . ((&lines * 27 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 104 + 59) / 119)
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
1resize 55|vert 1resize 14|2resize 27|vert 2resize 104|3resize 27|vert 3resize 104|
tabnext 1
3wincmd w

" vim: ft=vim ro nowrap smc=128
