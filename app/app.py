from flask import Flask, render_template, request
from glob import glob
import base64
import wave
import sys,os
import numpy as np
from feature_engineer import FeatureExtractor
from pydub import AudioSegment


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('hello.html', tite="flask test", name=name)

@app.route('/monomane')
def monomane():
    sound_list = glob('static/sound/*')
    sound_list = [i.split('/')[-1].replace('.mp3', '') for i in sound_list]
    print('sound_list:\n', sound_list)
    return render_template('monomane.html', sound_list=sound_list)


@app.route('/monomane_result', methods=['POST'])
def monomane_result():
    data = request.form['audio'].replace('data:audio/wav;base64,', '')
    # print('data:\n', data)

    wav_path='static/sound/sample.wav'
    try:
        with open(wav_path, "wb") as f:
            f.write(base64.b64decode(data))
    except:
        print("アップロード失敗")

    # サンプリング周波数 [Hz]
    sample_frequency = 16000
    # フレーム長 [ミリ秒]
    frame_length = 25
    # フレームシフト [ミリ秒]
    frame_shift = 10
    # 低周波数帯域除去のカットオフ周波数 [Hz]
    low_frequency = 20
    # 高周波数帯域除去のカットオフ周波数 [Hz]
    high_frequency = sample_frequency / 2
    # メルフィルタバンクの数
    num_mel_bins = 23
    # MFCCの次元数
    num_ceps = 13
    # ディザリングの係数
    dither=1.0
    ###特徴量抽出
    feat_extractor = FeatureExtractor(
        sample_frequency=sample_frequency, 
                       frame_length=frame_length, 
                       frame_shift=frame_shift, 
                       num_mel_bins=num_mel_bins, 
                       num_ceps=num_ceps,
                       low_frequency=low_frequency, 
                       high_frequency=high_frequency, 
                       dither=dither
    )

    try:        
        # wavファイルを読み込み，特徴量を計算する
        with wave.open(wav_path) as wav:
            # サンプリング周波数のチェック
            if wav.getframerate() != sample_frequency:
                sys.stderr.write('The expected \
                    sampling rate is 16000.\n')
                print(wav.getframerate())
                exit(1)
            # wavファイルが1チャネル(モノラル)
            # データであることをチェック
            # if wav.getnchannels() != 1:
            #     print(wav.getnchannels())
            #     sys.stderr.write('This program \
            #         supports monaural wav file only.\n')
            #     exit(1)
            
            # wavデータのサンプル数
            num_samples = wav.getnframes()

            # wavデータを読み込む
            waveform = wav.readframes(num_samples)

            # 読み込んだデータはバイナリ値
            # (16bit integer)なので，数値(整数)に変換する
            waveform = np.frombuffer(waveform, dtype=np.int16)
            
            # MFCCを計算する
            mfcc = feat_extractor.ComputeMFCC(waveform)

            # 特徴量のフレーム数と次元数を取得
            (num_frames, num_dims) = np.shape(mfcc)

            # 特徴量ファイルの名前(splitextで拡張子を取り除いている)
            out_file = os.path.splitext(os.path.basename(wav_path))[0]
            # out_file = os.path.join(os.path.abspath(out_dir), 
            #                         out_file + '.bin')

            # データをfloat32形式に変換
            mfcc = mfcc.astype(np.float32)
            print("mfcc:",mfcc)
            # データをファイルに出力
            # mfcc.tofile(out_file)
            # 発話ID，特徴量ファイルのパス，フレーム数，
            # 次元数を特徴量リストに書き込む
            # file_feat.write("%s %s %d %d\n" %
            #     (utterance_id, out_file, num_frames, num_dims))
            print(mfcc.shape)
    except:
        print("特徴量抽出失敗")
    ###距離計算



    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

