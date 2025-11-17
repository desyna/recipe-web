// import React, { useState } from 'react';
// import Image from 'next/image';

// export default function Home() {
//   const [tab, setTab] = useState('home');
//   const [selectedImage, setSelectedImage] = useState(null);
//   const [detectedImageUrl, setDetectedImageUrl] = useState(null);
//   const [ingredients, setIngredients] = useState([]);
//   const [recommendations, setRecommendations] = useState([]);
//   const [loading, setLoading] = useState(false);

//   const handleImageChange = (e) => {
//     const file = e.target.files?.[0];
//     if (file) setSelectedImage(file);
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     const file = e.dataTransfer.files?.[0];
//     if (file) setSelectedImage(file);
//   };

//   const handleDragOver = (e) => {
//     e.preventDefault();
//   };

//   const handleProcess = async () => {
//     if (!selectedImage) return;
//     setLoading(true);

//     const formData = new FormData();
//     formData.append('image', selectedImage);

//     const detectRes = await fetch('http://127.0.0.1:5000/detect', {
//       method: 'POST',
//       body: formData,
//     });
//     const detectData = await detectRes.json();
//     setDetectedImageUrl(`http://127.0.0.1:5000${detectData.image_url}`);
//     setIngredients(detectData.ingredients);

//     const recommendRes = await fetch('http://127.0.0.1:5000/recommend', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ ingredients: detectData.ingredients }),
//     });
//     const recommendData = await recommendRes.json();
//     setRecommendations(recommendData.recommendations);

//     setLoading(false);
//   };

//   return (
//     <main className="min-h-screen bg-black text-white">
//       <nav className="flex justify-between items-center p-6 border-b border-gray-700">
//         <h1 className="text-2xl font-bold">ResepApp</h1>
//         <div className="space-x-6">
//           <button onClick={() => setTab('home')} className={`hover:underline ${tab === 'home' ? 'font-bold' : ''}`}>
//             Home
//           </button>
//           <button onClick={() => setTab('recommendation')} className={`hover:underline ${tab === 'recommendation' ? 'font-bold' : ''}`}>
//             Recommendation
//           </button>
//         </div>
//       </nav>

//       {/* HOME */}
//       {tab === 'home' && (
//         <section className="text-center p-10">
//           <h2 className="text-xl mb-4">Selamat datang di ResepApp</h2>
//           <p className="mb-6">Sistem ini akan mendeteksi bahan dari gambar lalu memberikan rekomendasi resep berdasarkan bahan tersebut.</p>
//           <button onClick={() => setTab('recommendation')} className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded text-white">
//             Mulai Rekomendasi
//           </button>
//         </section>
//       )}

//       {/* RECOMMENDATION */}
//       {tab === 'recommendation' && (
//         <section className="grid md:grid-cols-2 gap-6 p-6">

//           <div>
//             <h2 className="text-xl mb-2 font-semibold">Rekomendasi Resep</h2>
//             {recommendations.length === 0 ? (
//               <p className="text-gray-400">Belum ada rekomendasi. Silakan unggah gambar terlebih dahulu.</p>
//             ) : (
//               recommendations.map((rec, i) => (
//                 <div key={i} className="border border-gray-700 p-4 mb-4 rounded shadow">
//                   <a href={rec.URL} target="_blank" rel="noopener noreferrer">
//                     <h3 className="text-lg font-bold text-green-400 underline mb-1">{rec.Title}</h3>
//                   </a>
//                   <p>
//                     <strong>Bahan:</strong> {rec.Ingredients}
//                   </p>
//                   <p>
//                     <strong>Love:</strong> ❤️ {rec.Loves}
//                   </p>
//                   <p>
//                     <strong>Skor Kecocokan:</strong> {rec.score.toFixed(4)}
//                   </p>
//                 </div>
//               ))
//             )}
//           </div>

//           <div>
//             <h2 className="text-xl mb-2 font-semibold">Upload Gambar Bahan</h2>

//             <div
//               onDrop={handleDrop}
//               onDragOver={handleDragOver}
//               onClick={() => document.getElementById('fileInput').click()}
//               className="w-full h-64 border-2 border-dashed border-gray-400 rounded-lg flex items-center justify-center relative cursor-pointer hover:border-green-500 transition-all overflow-hidden bg-gray-800"
//             >
//               <input id="fileInput" type="file" accept="image/*" onChange={handleImageChange} className="hidden" />

//               {selectedImage ? (
//                 <img src={URL.createObjectURL(selectedImage)} alt="Preview" className="max-h-full max-w-full object-contain p-4" />
//               ) : (
//                 <span className="text-gray-400 text-center px-4">Klik atau tarik gambar ke sini untuk mengunggah</span>
//               )}
//             </div>

//             <button onClick={handleProcess} className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded text-white mt-4">
//               Proses Gambar
//             </button>

//             {loading && <p className="text-green-400 mt-2">Memproses gambar dan mencari resep...</p>}

//             {detectedImageUrl && (
//               <div className="mt-6">
//                 <h3 className="font-semibold">Hasil Deteksi:</h3>
//                 <Image src={detectedImageUrl} alt="Detected" width={400} height={400} className="rounded shadow-lg mt-2" />
//                 <ul className="mt-2 list-disc list-inside">
//                   {ingredients.map((ing, i) => (
//                     <li key={i}>{ing}</li>
//                   ))}
//                 </ul>
//               </div>
//             )}
//           </div>
//         </section>
//       )}
//     </main>
//   );
// }

// import React, { useState, useRef } from 'react';
// import Image from 'next/image';

// export default function Home() {
//   const [tab, setTab] = useState('home');
//   const [selectedImage, setSelectedImage] = useState(null);
//   const [detectedImageUrl, setDetectedImageUrl] = useState(null);
//   const [ingredients, setIngredients] = useState([]);
//   const [recommendations, setRecommendations] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [showCamera, setShowCamera] = useState(false);
//   const videoRef = useRef(null);

//   const handleImageChange = (e) => {
//     const file = e.target.files?.[0];
//     if (file) setSelectedImage(file);
//   };

//   const handleProcess = async () => {
//     if (!selectedImage) return;
//     setLoading(true);

//     const formData = new FormData();
//     formData.append('image', selectedImage);

//     const detectRes = await fetch('http://127.0.0.1:5000/detect', {
//       method: 'POST',
//       body: formData,
//     });
//     const detectData = await detectRes.json();
//     setDetectedImageUrl(`http://127.0.0.1:5000${detectData.image_url}`);
//     setIngredients(detectData.ingredients);

//     const recommendRes = await fetch('http://127.0.0.1:5000/recommend', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ ingredients: detectData.ingredients }),
//     });
//     const recommendData = await recommendRes.json();
//     console.log('Hasil rekomendasi:', recommendData);
//     setRecommendations(recommendData.recommendations || []);

//     setLoading(false);
//   };

//   const startCamera = () => {
//     setShowCamera(true);
//     navigator.mediaDevices
//       .getUserMedia({ video: true })
//       .then((stream) => {
//         videoRef.current.srcObject = stream;
//       })
//       .catch((err) => {
//         console.error('Error accessing camera:', err);
//       });
//   };

//   const captureImage = () => {
//     const canvas = document.createElement('canvas');
//     canvas.width = videoRef.current.videoWidth;
//     canvas.height = videoRef.current.videoHeight;
//     canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
//     canvas.toBlob((blob) => {
//       const file = new File([blob], 'captured.png', { type: 'image/png' });
//       setSelectedImage(file);
//       stopCamera();
//     });
//   };

//   const stopCamera = () => {
//     const stream = videoRef.current.srcObject;
//     const tracks = stream.getTracks();
//     tracks.forEach((track) => track.stop());
//     setShowCamera(false);
//   };

//   return (
//     <main className="min-h-screen bg-black text-white">
//       <nav className="flex justify-between items-center p-6 border-b border-gray-700">
//         <h1 className="text-2xl font-bold">ResepApp</h1>
//         <div className="space-x-6">
//           <button onClick={() => setTab('home')} className={`hover:underline ${tab === 'home' ? 'font-bold' : ''}`}>
//             Home
//           </button>
//           <button onClick={() => setTab('recommendation')} className={`hover:underline ${tab === 'recommendation' ? 'font-bold' : ''}`}>
//             Recommendation
//           </button>
//         </div>
//       </nav>

//       {tab === 'home' && (
//         <section className="text-center p-10">
//           <h2 className="text-xl mb-4">Selamat datang di ResepApp</h2>
//           <p className="mb-6">Sistem ini akan mendeteksi bahan dari gambar lalu memberikan rekomendasi resep berdasarkan bahan tersebut.</p>
//           <button onClick={() => setTab('recommendation')} className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded text-white">
//             Mulai Rekomendasi
//           </button>
//         </section>
//       )}

//       {tab === 'recommendation' && (
//         <section className="grid md:grid-cols-2 gap-6 p-6">
//           <div>
//             <h2 className="text-xl mb-2 font-semibold">Rekomendasi Resep</h2>
//             {recommendations.length === 0 ? (
//               <p className="text-gray-400">Belum ada rekomendasi. Silakan unggah gambar terlebih dahulu.</p>
//             ) : (
//               recommendations.map((rec, i) => (
//                 <div key={i} className="border border-gray-700 p-4 mb-4 rounded shadow">
//                   <a href={rec.URL} target="_blank" rel="noopener noreferrer">
//                     <h3 className="text-lg font-bold text-green-400 underline mb-1">{rec.Title}</h3>
//                   </a>
//                   <p>
//                     <strong>Bahan:</strong> {rec.Ingredients}
//                   </p>
//                   <p>
//                     <strong>Love:</strong> ❤️ {rec.Loves}
//                   </p>
//                   <p>
//                     <strong>Skor Kecocokan:</strong> {rec.score.toFixed(4)}
//                   </p>
//                 </div>
//               ))
//             )}
//           </div>

//           <div>
//             <h2 className="text-xl mb-2 font-semibold">Ambil Gambar Bahan</h2>

//             <div onClick={startCamera} className="w-full h-64 border-2 border-dashed border-gray-400 rounded-lg flex items-center justify-center relative cursor-pointer hover:border-green-500 transition-all overflow-hidden bg-gray-800">
//               {showCamera ? (
//                 <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover" />
//               ) : selectedImage ? (
//                 <img src={URL.createObjectURL(selectedImage)} alt="Preview" className="max-h-full max-w-full object-contain p-4" />
//               ) : (
//                 <span className="text-gray-400 text-center px-4">Klik untuk membuka kamera</span>
//               )}
//             </div>

//             {showCamera && (
//               <div className="mt-2 flex gap-2">
//                 <button onClick={captureImage} className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-white">
//                   Ambil Foto
//                 </button>
//                 <button onClick={stopCamera} className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-white">
//                   Tutup Kamera
//                 </button>
//               </div>
//             )}

//             <button onClick={() => document.getElementById('fileInput').click()} className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded text-white mt-4">
//               Upload Gambar
//             </button>
//             <input id="fileInput" type="file" accept="image/*" onChange={handleImageChange} className="hidden" />

//             <button onClick={handleProcess} className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded text-white mt-4 ml-2">
//               Proses Gambar
//             </button>

//             {loading && <p className="text-green-400 mt-2">Memproses gambar dan mencari resep...</p>}

//             {detectedImageUrl && (
//               <div className="mt-6">
//                 <h3 className="font-semibold">Hasil Deteksi:</h3>
//                 <Image src={detectedImageUrl} alt="Detected" width={400} height={400} className="rounded shadow-lg mt-2" />
//                 <ul className="mt-2 list-disc list-inside">
//                   {ingredients.map((ing, i) => (
//                     <li key={i}>{ing}</li>
//                   ))}
//                 </ul>
//               </div>
//             )}
//           </div>
//         </section>
//       )}
//     </main>
//   );
// }

import React, { useState, useRef, useEffect } from 'react';
import Image from 'next/image';

export default function Home() {
  const [tab, setTab] = useState('home');
  const [selectedImage, setSelectedImage] = useState(null);
  const [detectedImageUrl, setDetectedImageUrl] = useState(null);
  const [ingredients, setIngredients] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/categories')
      .then((res) => res.json())
      .then((data) => setCategories(data.categories || []));
  }, []);

  useEffect(() => {
    if (ingredients.length > 0) {
      fetchRecommendations();
    }
  }, [selectedCategory]);

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) setSelectedImage(file);
  };

  const handleProcess = async () => {
    if (!selectedImage) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('image', selectedImage);

    const detectRes = await fetch('http://127.0.0.1:5000/detect', {
      method: 'POST',
      body: formData,
    });
    const detectData = await detectRes.json();
    setDetectedImageUrl(`http://127.0.0.1:5000${detectData.image_url}`);
    setIngredients(detectData.ingredients);

    await fetchRecommendations(detectData.ingredients);
    setLoading(false);
  };

  const fetchRecommendations = async (detectedIngredients = ingredients) => {
    const recommendRes = await fetch('http://127.0.0.1:5000/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients: detectedIngredients, category: selectedCategory }),
    });
    const recommendData = await recommendRes.json();
    setRecommendations(recommendData.recommendations || []);
  };

  const startCamera = () => {
    setShowCamera(true);
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch((err) => console.error(err));
  };

  const captureImage = () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
    canvas.toBlob((blob) => {
      const file = new File([blob], 'captured.png', { type: 'image/png' });
      setSelectedImage(file);
      stopCamera();
    });
  };

  const stopCamera = () => {
    const stream = videoRef.current.srcObject;
    stream?.getTracks().forEach((track) => track.stop());
    setShowCamera(false);
  };

  return (
    <main className="min-h-screen bg-black text-white">
      <nav className="flex justify-between items-center p-6 border-b border-gray-700">
        <h1 className="text-2xl font-bold">ResepApp</h1>
        <div className="space-x-6">
          <button onClick={() => setTab('home')} className={tab === 'home' ? 'font-bold underline' : ''}>
            Home
          </button>
          <button onClick={() => setTab('recommendation')} className={tab === 'recommendation' ? 'font-bold underline' : ''}>
            Recommendation
          </button>
        </div>
      </nav>

      {tab === 'home' && (
        <section className="text-center p-10">
          <h2 className="text-xl mb-4">Selamat datang di ResepApp</h2>
          <p className="mb-6">Deteksi bahan dari gambar dan merekomendasi resep.</p>
          <button onClick={() => setTab('recommendation')} className="bg-green-600 px-6 py-3 rounded">
            Mulai
          </button>
        </section>
      )}

      {tab === 'recommendation' && (
        <section className="grid md:grid-cols-2 gap-6 p-6">
          <div>
            <h2 className="text-xl font-semibold mb-2">Kategori:</h2>
            <select className="border border-white text-white bg-gray-800 p-2 mb-4 rounded" value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
              <option value="">Semua Kategori</option>
              {categories.map((cat, i) => (
                <option key={i} value={cat.toLowerCase()}>
                  {cat}
                </option>
              ))}
            </select>

            <h2 className="text-xl font-semibold mb-2">Rekomendasi Resep</h2>
            {recommendations.length === 0 ? (
              <p className="text-gray-400">Belum ada rekomendasi.</p>
            ) : (
              recommendations.map((rec, i) => (
                <div key={i} className="bg-gray-900 p-4 rounded mb-4 shadow">
                  <a href={rec.URL} className="text-green-400 underline font-bold" target="_blank">
                    {rec.Title}
                  </a>
                  <p>
                    <strong>Kategori:</strong> {rec.Category}
                  </p>
                  <p>
                    <strong>Bahan:</strong> {rec.Ingredients}
                  </p>
                  <p>
                    <strong>Love:</strong> ❤️ {rec.Loves}
                  </p>
                  <p>
                    <strong>Skor:</strong> {rec.score.toFixed(4)}
                  </p>
                </div>
              ))
            )}
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2">Ambil Gambar</h2>

            <div onClick={startCamera} className="border-2 border-dashed rounded h-64 flex justify-center items-center cursor-pointer">
              {showCamera ? (
                <video ref={videoRef} autoPlay className="w-full h-full object-cover" />
              ) : selectedImage ? (
                <img src={URL.createObjectURL(selectedImage)} alt="preview" className="object-contain max-h-full" />
              ) : (
                <span className="text-gray-400">Klik untuk buka kamera</span>
              )}
            </div>

            {showCamera && (
              <div className="mt-2 flex gap-2">
                <button onClick={captureImage} className="bg-green-600 px-4 py-2 rounded">
                  Ambil
                </button>
                <button onClick={stopCamera} className="bg-red-600 px-4 py-2 rounded">
                  Tutup
                </button>
              </div>
            )}

            <input type="file" className="hidden" id="fileInput" accept="image/*" onChange={handleImageChange} />
            <button onClick={() => document.getElementById('fileInput').click()} className="bg-blue-600 px-6 py-2 mt-4 rounded">
              Upload
            </button>
            <button onClick={handleProcess} className="bg-green-600 px-6 py-2 mt-2 rounded ml-2">
              Proses
            </button>

            {loading && <p className="mt-2 text-green-400">Memproses gambar...</p>}
            {detectedImageUrl && (
              <div className="mt-4">
                <h3 className="font-semibold">Hasil Deteksi:</h3>
                <Image src={detectedImageUrl} alt="detected" width={400} height={400} className="rounded mt-2" />
                <ul className="list-disc pl-6">
                  {ingredients.map((ing, i) => (
                    <li key={i}>{ing}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </section>
      )}
    </main>
  );
}
