# -*- coding: utf-8 -*-

# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Add-on: Tempus Playlist
# Author: ad, whufclee

#----------------------------------------------------------------
import urllib
import urllib2
import datetime
import shutil
import os
import xbmcvfs
import traceback
import cookielib
import requests
import xbmc
import xbmcaddon
import xbmcplugin
import re
import xbmcgui

from koding import route, Add_Dir, Addon_Setting, Data_Type, Find_In_Text
from koding import Open_URL, OK_Dialog, Open_Settings, Play_Video, Run, Text_File

resolve_url=['alldebrid.com', 'allmyvideos.net', 'estream.to',  'xvidstage.com', 'streamango.com','vidto.me',  '1fichier.com','allvid.ch', 'auengine.com', 'fmovies.se','beststreams.net', 'briskfile.com', 'castamp.com', 'clicknupload.com', 'clicknupload.me', 'clicknupload.link', 'cloudy.ec', 'cloudzilla.to', 'neodrive.co', 'crunchyroll.com', 'daclips.in', 'daclips.com', 'dailymotion.com', 'divxstage.eu', 'divxstage.net', 'divxstage.to', 'couldtime.to', 'ecostream.tv', 'exashare.com', 'facebook.com', 'fastplay.sx', 'filehoot.com', 'filenuke.com', 'filepup.net', 'filmshowonline.net', 'flashx.tv', 'plus.google.com', 'googlevideo.com', 'picasaweb.google.com', 'googleusercontent.com', 'googledrive.com', 'gorillavid.in', 'gorillavid.com', 'gorillavid.in', 'grifthost.com', 'hugefiles.net', 'idowatch.net', 'indavideo.hu', 'ishared.eu', 'jetload.tv', 'movie4k.tv', 'yourupload.com', 'kingfiles.net', 'letwatch.us', 'letwatch.to', 'vidshare.us', 'mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'api.video.mail.ru', 'mega-debrid.eu', 'megamp4.net', 'mersalaayitten.com', 'movdivx.com', 'movpod.net', 'movpod.in', 'movshare.net', 'wholecloud.net', 'mp4engine.com', 'mp4stream.com', 'mp4upload.com', 'myvidstream.net', 'nosvideo.com', 'noslocker.com', 'auroravid.to', 'novamov.com', 'nowvideo.sx', 'nowvideo.eu', 'nowvideo.ch', 'nowvideo.sx', 'nowvideo.co', 'nowvideo.li', 'nowvideo.ec', 'nowvideo.at', 'nowvideo.fo', 'ok.ru', 'odnoklassniki.ru', 'openload.io', 'openload.co', 'play44.net', 'played.to', 'playhd.video', 'playhd.fo', 'playu.net', 'playu.me', 'playwire.com', 'Premiumize.me', 'primeshare.tv', 'promptfile.com', 'purevid.com', 'rapidvideo.ws', 'rapidvideo.com', 'api.real-debrid.com', 'premium.rpnet.biz', 'rutube.ru', 'shared2.me', 'shared.sx', 'sharerepo.com', 'sharesix.com', 'simply-debrid.com', 'speedplay.xyz', 'speedplay.us', 'speedplay3.pw', 'speedvideo.net', 'stagevu.com', 'streamcloud.eu', 'streamin.to', 'teramixer.com', 'thevideo.me', 'thevideos.tv', 'toltsd-fel.tk', 'trollvid.net', 'tune.pk', 'tusfiles.net', 'twitch.tv', 'up2stream.com', 'upload.af', 'uploadc.com', 'uploadc.ch', 'zalaa.com', 'uploadx.org', 'uptobox.com', 'uptostream.com', 'userfiles.com', 'userscloud.com', 'veehd.com', 'veoh.com', 'vid.ag', 'vidbull.com', 'vidcrazy.net', 'uploadcrazy.net', 'thevideobee.to', 'videoboxer.co', 'vidgg.to', 'vid.gg', 'videohut.to', 'videomega.tv', 'videoraj.to', 'videorev.cc', 'videosky.to', 'video.tt', 'videoweed.es', 'bitvid.sx', 'videoweed.com', 'videowood.tv', 'byzoo.org', 'playpanda.net', 'videozoo.me', 'videowing.me', 'videowing.me', 'easyvideo.me', 'play44.net', 'playbb.me', 'video44.net', 'vidio.sx', 'vid.me', 'vidspot.net', 'vidto.me', 'vidup.me', 'vidup.org', 'vidzi.tv', 'vimeo.com', 'vivo.sx', 'vk.com', 'vkpass.com', 'vodlocker.com', 'vshare.io', 'vshare.eu', 'watchers.to', 'watchonline.to', 'watchvideo.us', 'watchvideo2.us', 'watchvideo3.us', 'watchvideo4.us', 'watchvideo5.us', 'watchvideo6.us', 'watchvideo7.us', 'watchvideo8.us', 'watchvideo9.us', 'weshare.me', 'xvidstage.com', 'youlol.biz', 'shitmovie.com', 'yourupload.com', 'youtube.com', 'youtu.be', 'youwatch.org', 'api.zevera.com', 'zettahost.tv', 'zstream.to']

#----------------------------------------------------------------

debug        = Addon_Setting(setting='debug')       
addon_id     = xbmcaddon.Addon().getAddonInfo('id') 
home         = xbmc.translatePath('special://home') 


main_xml     = 'https://raw.githubusercontent.com/bentkatu/repository.atrain/master/plugin.video.tempusmovies/resources/main.xml'

@route(mode='start')
def Start():
    Main_Menu(main_xml)
#----------------------------------------------------------------
@route(mode='main_menu',args=['url'])
def Main_Menu(url=main_xml):

    if debug == 'true':
        Add_Dir ( '[COLOR=lime]Koding Tutorials[/COLOR]', '', "tutorials", True, '', '', '' )

    if url.startswith('http'):
        contents  = Open_URL(url)
    else:
        contents  = Text_File(url,'r')

    contents = contents.replace('\n','').replace('\t','')

    raw_links = Find_In_Text(content=contents, start='<item>', end=r'</item>')
    xbmc.log(repr(raw_links),2)
    counter = 1

    for item in raw_links:
        xbmc.log('# Checking link %s'%counter,2)
        counter += 1
        title  = Find_In_Text(content=item, start='<title>', end=r'</title>')
        title  = title[0] if (title!=None) else 'Unknown Video'
        thumb  = Find_In_Text(content=item, start='<thumbnail>', end=r'</thumbnail>')
        thumb  = thumb[0] if (thumb!=None) else ''
        fanart = Find_In_Text(content=item, start='<thumbnail>', end=r'</thumbnail>')
        fanart = fanart[0] if (fanart!=None) else ''

        if not '<sublink>' in item:
            links  = Find_In_Text(content=item, start='<link>', end=r'</link>')

        else:
            links  = Find_In_Text(content=item, start='<sublink>', end=r'</sublink>')

        if links[0].endswith('.xml') or links[0]=='none' or links[0] == '' or links[0].startswith('msg~'):
            links = links[0]

        if links == 'none' or links == '':
            Add_Dir( name=title, url='', mode='', folder=False, icon=thumb, fanart=fanart )

        elif Data_Type(links)=='str':

            if links.startswith('msg~'):
                links = links.replace('msg~','')
                Add_Dir( name=title, url="{%s}"%links, mode='simple_dialog', folder=False, icon=thumb, fanart=fanart )
            else:
                Add_Dir( name=title, url=links, mode='main_menu', folder=True, icon=thumb, fanart=fanart )

        else:
            Add_Dir( name=title, url="{'url':%s}"%links, mode='play_link', folder=False, icon=thumb, fanart=fanart )

@route(mode='play_link',args=['url'])
def Play_Link(url):
    if len(url)==1:
        if not Play_Video(url[0]):
            OK_Dialog( 'PLAYBACK FAILED','This stream is currently offline.' )

    elif len(url)>1:
        link_list   = []
        counter     = 1
        for item in url:
            link_list.append( 'Link '+str(counter) )
            counter += 1
        choice = Select_Dialog( 'CHOOSE STREAM', link_list )
        if choice >= 0:
            if not Play_Video( url[choice] ):
                OK_Dialog( 'PLAYBACK FAILED','This stream is currently offline.' )
                Play_Link(url)

@route(mode='koding_settings')
def Koding_Settings():
    Open_Settings()

@route(mode='simple_dialog', args=['title','msg'])
def Simple_Dialog(title,msg):
    OK_Dialog(title, msg)

if __name__ == "__main__":
    Run(default='start')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))