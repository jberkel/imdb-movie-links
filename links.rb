#!/usr/bin/env ruby

def parse(verb = 'references')
  refs = {}
  started = false
  title = nil
  STDIN.readlines.each do |line|
    l = line.force_encoding('iso-8859-1').chop
    next if l.length == 0

    # skip headers
    unless started
       next if l != '================'
       started = true
       next
    end

    if l[0] != ' '
      title = l
    elsif l =~ /\s+\(#{verb} (.+)\)\Z/
      (refs[title] ||= []) << $1
    end
  end
  refs
end

def escape(s)
  if s.include?('"') || s.include?('|')
    '"' + s.gsub(/"/) { |m| '""' } + '"'
  else
    s
  end.encode('UTF-8')
end

if __FILE__ == $0
  type = ARGV[0] || 'references'
  links = parse(type)
  File.open("#{type}.csv", 'w') do |f|
    links.each do |title, refs|
      f.puts ([title] + refs).map { |s| escape(s) }.join('|')
    end
  end
end
