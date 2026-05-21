require 'json'

use_random_seed 1001

use_osc "127.0.0.1", 4559     # send outgoing OSC to your Python server
count = 0
with_fx :level, amp: 0.5 do
  live_loop :test do
    const = 0
    C = [
      chord(:A4, :major).to_a,
      chord(:D4, :major).to_a,
      chord(:E4, :major).to_a,
      chord(:A4, :major).to_a,
      chord(:B3, :minor).to_a,
      chord(:E3, :major).to_a,
      chord(:A4, :major).to_a,
      chord(:A4, :major).to_a,
      chord(:E3, :major).to_a,
      chord(:A4, :major).to_a,
      chord(:Db4, :minor).to_a,
      chord(:D4, :major).to_a,
      chord(:E4, :major).to_a,
      chord(:E4, :major).to_a,
      chord(:E4, :major).to_a,
      chord(:Gb4, :minor).to_a,
      chord(:A4, :major).to_a,
      chord(:D4, :major).to_a,
    ]
    if count < 1
      increment = 2
    elsif count < 2
      increment = 498
    else
      increment = 100
    end
    
    count = count + 1
    puts count
    puts increment
    
    use_synth :organ_tonewheel
    play [:E3+ const, :E2+ const , :E4+ const, :E1+ const, :E5+ const]
    sample :drum_cymbal_open, amp: 0.05, rate: 0.5
    sample :drum_bass_hard, amp: 0.08
    
    puts "▶ firing"
    osc "/py_request", C.to_json, increment
    
    # leave this line alone and run:
    notes = sync "/osc*/python_reply"
    notes = notes.each_slice(C.length).to_a
    
    if count > 12
      sleep 10000
    end
    
    
    use_bpm 120
    cutoff_val = 70
    amp_val = 0.2
    print(notes)
    (notes[0].length).times do |t|
      
      use_synth :organ_tonewheel
      # glue and space
      
      with_fx :lpf, cutoff: 100 do                # roll off any icy highs
        with_fx :reverb, room: 0.35, mix: 0.25 do  # a bit more space
          with_fx :compressor, threshold: 0.2, slope_above: 0.5 do
            # Slow breathing wobble
            with_fx :tremolo, phase: 8, depth: 0.7, mix: 0.5 do
              # Fast choppy wobble
              with_fx :tremolo, phase: 0.5, depth: 0.5, mix: 0.4 do
                with_fx :echo, phase: 0.375, decay: 2, mix: 0.15 do
                  
                  use_synth :sine
                  use_synth_defaults \
                    attack:  0.05,
                    sustain: 2,
                    release: 0.4,
                    amp:     1
                  play notes[0][t] +const, amp: 0.15
                  
                end
              end
            end
          end
        end
      end
      
      
      with_fx :compressor, threshold: 0.2, slope_above: 0.5, clamp_time: 0.03, relax_time: 0.1 do
        with_fx :reverb, room: 0.4, mix: 0.25 do
          # Main organ stab
          use_synth :hollow
          play [notes[1][t] +const, notes[2][t] +const],
            attack: 0.5,    # slow-ish fade-in for smoothness
            sustain: 3,    # hold the chord for 3 beats
            release: 1,    # gentle tail
            amp: 1.2,
            pan: rrand(-0.1, 0.1)
          
          # Underlying pad layer for warmth
          use_synth :sine
          play [notes[1][t] +const, notes[2][t] +const],
            attack: 1,      # very slow fade-in
            sustain: 3,
            release: 1.5,
            amp: 0.4
        end
      end
      
      with_fx :compressor, threshold: 0.2, slope_above: 0.5, clamp_time: 0.03, relax_time: 0.1 do
        with_fx :reverb, room: 0.3, mix: 0.15 do
          use_synth :fm
          # default params for that bell-y electric-piano-ish tone
          use_synth_defaults depth:   0.6,
            divisor: 3,
            attack:  0.005,
            sustain: 0.1,
            release: 0.1,
            cutoff:  90,
            amp:     1.3
          play notes[2][t] +const
        end
      end
      
      use_synth_defaults
      with_fx :reverb, room: 0.8, mix: 0.5 do      # big, lush space
        with_fx :echo, phase: 0.25, mix: 0.3 do    # subtle repeats for depth
          use_synth :fm
          play notes[3][t] +const, release: 2, amp: 0.3,
            depth: 2, divisor: 1                # fat FM bass voice
        end
      end
      sleep 4
      
      
    end
  end
end




live_loop :nother do
  if count > 24
    sleep 100000
  end
  if count > 12
    count = count + 1
    use_bpm 120
    C = [
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
      chord(:A4, '7').to_a,
      chord(:Bb4, '7').to_a,
    ]
    osc "/py_request", C.to_json, 500
    
    pattern1 = spread(rand_i(6)+1, rand_i(8)+1)
    pattern2 = spread(rand_i(2)+1, rand_i(5)+1)
    pattern3 = spread(rand_i(4)+1, rand_i(7), rotate: rand_i(3))
    pattern4 = spread(rand_i(3), rand_i(4), rotate: rand_i(1))
    pattern5 = spread(2,8)
    pattern6 = spread(4,8, rotate: 2)
    
    # leave this line alone and run:
    notes = sync "/osc*/python_reply"
    notes = notes.each_slice(C.length).to_a
    
    (notes[0].length).times do |t|
      use_synth_defaults
      with_fx :reverb, room: 0.8, mix: 0.5 do      # big, lush space
        with_fx :echo, phase: 0.25, mix: 0.3 do    # subtle repeats for depth
          use_synth :fm
          play :A1, release: 2, amp: 0.15,
            depth: 2, divisor: 1 if t%2==0            # fat FM bass voice
          play :Bb1, release: 2, amp: 0.15,
            depth: 2, divisor: 1 if t%2==1            # fat FM bass voice
        end
      end
      use_synth_defaults
      
      # 16 beat measures
      16.times do
        play notes[0][t], amp: 0.05 if pattern1.tick
        play notes[1][t], amp: 0.05 if pattern2.look
        play notes[2][t], amp: 0.05 if pattern2.look
        play notes[3][t], amp: 0.05 if pattern2.look
        sample :drum_bass_hard, amp: 0.05 if pattern5.look
        sample :drum_snare_softm, amp: 0.05, cutoff: 80 if pattern6.look
        sleep 0.25
      end
    end
    
    
  end
  sleep 1
end



# Space vibes from chatGPT
define :space_vibes do |root=:e3, chord_type=:m9, duration=64|
  use_bpm 30  # slow pulse
  
  ## 1) Low drone
  in_thread do
    use_synth :sine
    with_fx :reverb, room: 0.8, mix: 0.7 do
      play root,
        attack:  duration / 2.0,
        sustain: duration,
        release: duration / 4.0,
        amp:     0.05
    end
  end
  
  ## 2) Soft pad chord
  in_thread do
    use_synth :prophet
    with_fx :reverb, room: 0.8, mix: 0.7 do
      play chord(root, chord_type),
        attack: 4,
        sustain: duration / 2.0,
        release: 4,
        cutoff:  80,
        amp:     0.04
    end
  end
  
  ## 3) Random shimmers
  in_thread do
    use_synth :dark_ambience
    elapsed = 0
    while elapsed < duration do
      play scale(root + 12, :minor_pentatonic).choose,
        attack:  1,
        sustain: 2,
        release: 4,
        amp:     0.03,
        pan:     rrand(-0.5, 0.5)
      d = [4, 8].choose
      sleep d
      elapsed += d
    end
  end
  
  ## 4) Gentle pulsing heartbeat
  in_thread do
    elapsed = 0
    while elapsed < duration do
      sleep 4
      elapsed += 4
      use_synth :hollow
      play root - 12,
        attack:  0.25,
        sustain: 0.5,
        release: 1,
        amp:     0.02
    end
  end
end

live_loop :last do
  if count > 26
    sleep 1000000
  end
  
  if count > 24
    C = [
      chord(:D4, :m9).to_a,
      chord(:D4, :m9).to_a,
      chord(:D4, :m9).to_a,
      chord(:D4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:F4, :M7).to_a.push(67),
      chord(:F4, :M7).to_a.push(67),
      chord(:F4, :M7).to_a.push(67),
      chord(:F4, :M7).to_a.push(67),
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:E4, :m9).to_a,
      chord(:D4, :m9).to_a,
      chord(:D4, :m9).to_a,
      chord(:D4, :m9).to_a,
      chord(:D4, :m9).to_a,
    ]
    osc "/py_request", C.to_json, 500
    use_bpm 60
    count = count + 1
    
    # leave this line alone and run:
    notes = sync "/osc*/python_reply"
    notes = notes.each_slice(C.length).to_a
    
    
    (notes[0].length).times do |t|
      if t < 5
        space_vibes :D3, :m9, 0.1
      elsif t< 9
        space_vibes :E3, :m9, 0.1
      elsif t < 13
        space_vibes :F3, :M7, 0.1
      elsif t < 17
        space_vibes :E3, :m9, 0.1
      else
        space_vibes :D3, :m9, 0.1
      end
      
      
      64.times do
        use_synth :kalimba
        play notes[rand_i(4)][t], amp: 0.4, cutoff: 80
        sleep 0.05
      end
      
    end
  end
  sleep 1
end


