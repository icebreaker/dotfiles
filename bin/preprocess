#!/usr/bin/env ruby 

def preprocess(text, *defines)
  data = text.dup

  #
  # Legend: 
  #
  #	$1 = ifdef or ifndef
  #	$2 = define
  #	$3 = block of text (may contain an #else which is 'parsed' separately below)
  #	$4 = endif
  #
  data.gsub!(/#(ifdef|ifndef)\s+(.*?)\s+(.*?)\s+#(endif)/m) do |m|
    define = $2.to_sym

    if $1 == 'ifdef'
      cond = defines.include?(define)
      if_content = $3
      else_content = ''
    else
      cond = !defines.include?(define)
      if_content = $3
      else_content = ''
    end

    #
    # Legend:
    #
    #	branch[1] = first block of text (if)
    #	branch[2] = else
    #	branch[3] = second block of text (endif)
    #
    branch = $3.match(/(.*?)\s+#(else)\s+(.*)/m)
    if branch
      if_content = branch[1]
      else_content = branch[3]
    end

    if cond
      if_content
    else
      else_content
    end
  end

  data
end

if ARGV.size < 1
	puts 'usage: preprocess -Ddefine -DdefineN < input > output'
	exit 1
end

defines = ARGV.select { |arg| arg.start_with?('-D') }.map { |arg| arg.delete('-D').to_sym }
STDOUT.write(preprocess(STDIN.read(), *defines))
