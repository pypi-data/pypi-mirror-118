class HRDPS_Cat(object):


        def __init__(self,parent) :
                pass

        def on_file(self,parent):


                import time
                import os.path
                import subprocess


                datestr = time.strftime(':%Y%m%d%H%M%S',time.localtime())
                listdir = "/d1/nnguyen/sarracenia/sarra/test4/"


                filename = str(parent.msg.new_file)
                parent.logger.info( 'filename = %s' % filename)
                filenamearr = filename.split("_")
                parent.logger.info( 'filenamearr = %s' % filenamearr )

                if len(filenamearr) < 3:
                        parent.logger.info( 'filenamearr not enough underscores')
                        return True

                newfile = "gem_10km."+filenamearr[-2][0:8]+".i"+filenamearr[-2][8:10]+"00.f"+filenamearr[-1][1:-6]+".grb2"
                parent.logger.info( 'newfile = %s' % newfile )


                p = subprocess.Popen("cat "+parent.msg.new_file+">>"+newfile,shell=True)
                p.wait()

                os.unlink( parent.msg.new_file )
                return True


hrdps_cat=HRDPS_Cat(self)

self.on_file=hrdps_cat.on_file



