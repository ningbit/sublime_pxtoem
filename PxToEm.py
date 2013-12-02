import sublime, sublime_plugin, re

def replace_px(css):
    # Example css: "width: 12px; /16"
    # grabs "12px"
    px_s = re.search(r'\d+px',css).group()

    # grabs 12
    px = int(re.search(r'\d+',px_s).group())

    # grabs /16 (base) or sets default to 16
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

    # generate new string with comment
    new_css = re.sub(r'\d+px',em,css,1)
    return re.sub(r'\s/\d+',"",new_css,1) + comment

class PxToEmCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            # grabs entire line from selection
            selection = self.view.line(region)
            css = self.view.substr(selection)

            if (re.search(r'px',css) == None):
                print("No px found")

            else:
                # check for multi-line selections
                css =  css.split("\n")
                new_css = ""

                # iterates through each line of css and calls replace_px, concats new_css with \n per new line
                for each_line in css:
                    while (re.search(r'px',each_line)):
                        each_line = replace_px(each_line)
                    new_css = new_css + each_line + "\n"

                self.view.replace(edit, selection, new_css.rstrip())                    
