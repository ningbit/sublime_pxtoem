import sublime, sublime_plugin, re

def new_css(css):
    # Example css: "width: 12px; /16"
    # grabs "12px"
    px_s = re.search(r'\d+px',css).group()

    # grabs 12
    px = int(re.search(r'\d+',px_s).group())

    # grabs 16 (base) or sets default to 16
    if re.search(r'/\d+',css) and re.search(r'/\d+',css).group():
        base_s = re.search(r'/\d+',css).group()
        base = int(re.search(r'\d+',base_s).group())
    else:
        base = 16

    # constructs "0.75em", omits decimal places if an integer
    em_num = px/float(base)
    em = str(em_num) + 'em' if (em_num != round(em_num)) else (str(int(em_num)) + 'em')

    # constructs comment /* 12/16 */, omits if comment is /* 16/16 */
    comment = "" if (base == px and base == 16) else " /* %s/%s */" % (px,base)
    # comment = " /* %s/%s */" % (px,base)

    # generate new string with comment
    new_css = re.sub(r'\d+px',em,css,1)
    new_css = re.sub(r'\s/\d+',"",new_css,1) + comment
    return new_css

class PxToEmCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():  
            # grabs entire line from selection
            line = self.view.line(region)
            css = self.view.substr(line)

            if css.find('\n') != -1:
                print "multiple line selection not supported"
            elif re.search(r'px.+px.+px.+px.+px',css):
                print "Invalid CSS: too many (px)'s to process"        
            elif re.search(r'px.+px.+px.+px',css):
                print "found 4 (px)'s"
                s = new_css(css)
                s = new_css(s)
                s = new_css(s)
                s = new_css(s)
                self.view.replace(edit, line, s)                   
            elif re.search(r'px.+px.+px',css):
                print "found 3 (px)'s"
                s = new_css(css)
                s = new_css(s)
                s = new_css(s)
                self.view.replace(edit, line, s)                
            elif re.search(r'px.+px',css):
                print "found 2 (px)'s"
                s = new_css(css)
                s = new_css(s)
                self.view.replace(edit, line, s)

            else:          
                self.view.replace(edit, line, new_css(css))