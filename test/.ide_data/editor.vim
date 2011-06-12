" ~/bl0b_dev/hack-ide/test/.ide_data/editor.vim: Vim session script.
" Created by ~/.vim/autoload/xolox/session.vim on 10 juin 2011 at 17:40:56.
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
cd ~/bl0b_dev/hack-ide/test
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 py/sandbox.py
badd +0 my.hackide
silent! argdel *
set lines=42 columns=74
edit my.hackide
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
exe 'vert 1resize ' . ((&columns * 16 + 37) / 74)
exe '2resize ' . ((&lines * 27 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 57 + 37) / 74)
exe '3resize ' . ((&lines * 12 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 57 + 37) / 74)
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
let s:l = 7 - ((6 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 031l
wincmd w
argglobal
edit py/sandbox.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 010l
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 16 + 37) / 74)
exe '2resize ' . ((&lines * 27 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 57 + 37) / 74)
exe '3resize ' . ((&lines * 12 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 57 + 37) / 74)
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
NERDTree ~/bl0b_dev/hack-ide/test
1resize 40|vert 1resize 16|2resize 27|vert 2resize 57|3resize 12|vert 3resize 57|
tabnext 1
2wincmd w

" vim: ft=vim ro nowrap smc=128
