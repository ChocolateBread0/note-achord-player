import numpy as np
import sounddevice as sd
import time
import math

def suona_tensore(tensore, sample_rate=44100, volume=0.1):
    
    wavet= 0; 
    wave = 0; 
    for freq, durata in tensore:
        
        if freq[0] == 0: # Handle silence/pause
            time.sleep(durata)
            continue
        
        # Generate the time index (time flowing)
        t = np.linspace(0, durata, int(sample_rate * durata), False)
        
        for i in range (0, len(freq), 1):
            # we have to generate a sinusoidal wave..
            # since sin(\vec{v}) = (sin(v_1), sin(v_2), ...., sin(v_n))^{T}
            k = 5/durata
            wavet += np.exp(-k*t)* np.sin(2 * np.pi * freq[i] * t); 
            
        # Prevent chords with many notes from sounding louder than single notes
        if len(freq) > 1:
            wavet = wavet / len(freq)    
        
        wave = volume * wavet; 
        wavet =0;  
        
        # 3. Play (non-blocking)
        sd.play(wave, sample_rate)
        
        # 4. Wait for the note to finish before moving to the next one
        sd.wait()

# This function takes notes e.g.: A3, G3# etc..
# and converts them into frequencies
# The piano has 88 keys and goes from A0 to C8
# all "C" represent 'Do' and so on

def Converti_inFreq (values):
    letters = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#","B"]
    Tensor = []; 
    freqVector = []; 
    position = 0; 
    temp = 0; 
    note = ""; 
    vnota = 0; 
    
    for i in range(0, len(values), 1):
        chord=values[i][0] # musical note
        temp = 0; 
        # if it's "00" then it's a pause
        if (chord != "00"):
            # from here I have to isolate the note because I could have a chord
            for j in range(0, len(chord), 1):
                # scroll through the string and separate letters from notes
                if (chord[j].isdigit()):                 
                    # take the difference between the current position and temp
                    note = chord[j-temp:j]
                    if note in  letters:
                        vnota = letters.index(note); 
                        
                        # 3 initial notes A0, A#0, B0 
                        # (vnota + 1) note number +1 because the array starts from 0
                        # 12 * (int(chord[j]) - 1) cause each octave has 12 notes.. 
                        # -1 because otherwise i would have had another one octave
                        position = 12 * (int(chord[j]) - 1) + vnota + 4; 
                        
                        pow = (position - 49)/12; 
                        frequence = 440 * math.pow(2, pow)
                        rfreq = int(frequence * 100) / 100
                        
                        freqVector.append(rfreq); 
                        #matrix.append([frequence, values[i][1]]); 
                    else:
                        print("Check how program trimmed string")
                    temp = -1; 
                temp += 1; 
            # i put it in a tensor
            Tensor.append([freqVector.copy(), values[i][1]]); 
            freqVector.clear();             
        else:
            freqVector.append(0); 
            Tensor.append([freqVector.copy(), values[i][1]]); 
            freqVector.clear();  

    return Tensor

def main():
    # insert the song and relative timing
    '''
    values = [
        #[note/chord, duration in seconds]
        #Still D.R.E.
        ["C5E5A5", 0.3], # this is a chord (notes must be attached)
        ["C5E5A5", 0.3],
        ["C5E5A5", 0.3],
        ["C5E5A5", 0.3],
        ["C5E5A5", 0.3],
        ["C5E5A5", 0.3],
        ["B4E5A5", 0.3],
        ["B4E5A5", 0.3],
        ["B4E5A5", 0.3],        
        ["B4E5G5", 0.3],
        ["B4E5G5", 0.3],  
        ["B4E5G5", 0.3], 
        ["B4E5G5", 0.3], 
        ["00", 0.5]  # double zero "00" means pause.. won't play for 0.5s
    ]'''
    
    values = [
    # [note/chord, duration in seconds]
    
    # moonlight sonata
    ["G#3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["A3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["A3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["A3", 0.4], ["D4", 0.4], ["F#4", 0.4],
    ["A3", 0.4], ["D4", 0.4], ["F#4", 0.4],
    ["G#3", 0.4], ["C4", 0.4], ["F#4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4], ["E4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4], ["D#4", 0.4],
    ["F#3", 0.4], ["C4", 0.4], ["D#4", 0.4],
    ["E3", 0.4],
    ["G#3", 0.4], ["C#4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4],["E4", 0.4],
    ["G#3", 0.4], ["C#4", 0.4],["E4", 0.4], ["G#4", 0.4],
    ["C#4", 0.4],["E4", 0.4], ["G#4", 0.1], ["G#4", 0.8],

    ["00", 0.5] # pauses
]
    
    tensor = Converti_inFreq(values); 
    # spits me out a tensor like:
    '''
    my_tensor = [
    [[440.0, 345.23, 680, 234, 123, 234, ....], 0.5],  # this is a chord
    [493.8, 0.5],  # B (single note)
    [523.2, 1.0],  # C
    [0, 0.2],      # Pause
    [392.0, 0.5]   # G
    ]
    
    '''
    suona_tensore(tensor); 
    
main()