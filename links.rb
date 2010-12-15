#!/usr/bin/env ruby

def parse(verb)
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

    if l[0..0] != ' '
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
  if RUBY_VERSION.to_f < 1.9
    raise "Ruby 1.9 required"
  end

  type = ARGV[0] || 'references'
  parse(type).each do |title, refs|
    puts ([title] + refs).map { |s| escape(s) }.join('|')
  end
end
