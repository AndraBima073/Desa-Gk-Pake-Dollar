import React, { use, useState, useEffect } from 'react';
import '../styles/LogiMatch.css';

const LogiMatch = () => {
    const [activeView, setActiveView] = useState('input');
    const [orders, setOrders] = useState([]);

    // State utk API & Form
    const [smartText, setSmartText] = useState('');
    const [formData, setFormData] = useState({ origin: '', destination: '', date: '', item_name: '', volume_m3: '', weight_tons: ''});
    const [matchData, setMatchData] = useState(null);

    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');
    const [showAlternatives, setShowAlternative] = useState(false);
    //const [shippingMode, setShippingMode] = useState('FCL');

    // Routes List
    const [routes, setRoutes] = useState([]);
    const [loadingRoutes, setLoadingRoutes] = useState(false);



// Fungsi Ekstraksi Teks (NLP)

const handleFetchRoutes = async () => {
    setLoadingRoutes(true);
    setErrorMsg('');

    try {
        const response = await fetch('http://api.andrabima.my.id/api/v1/routes');

        if (!response.ok) {
            throw new Error('Gagal mengambil daftar kapal.');
        }

        const data = await response.json();
        setRoutes(data);
    }

    catch (err) {
        console.log("Menggunakan fallback data routes untuk demo...");

        // Mock data jika server mati (DEMO UI)
        setRoutes([
            {
                origin: 'Jakarta',
                destination: 'Surabaya',
                date: '2026-07-29',
                available_volume_m3: 15,
                available_weight_tons: 10,
                space_utilization_percent: 60
            },
            {
                origin: 'Jakarta',
                destination: 'Makassar',
                date: '2026-08-02',
                available_volume_m3: 8,
                available_weight_tons: 5,
                space_utilization_percent: 85
            }
        ]);
    }

    setLoadingRoutes(false);
};

useEffect(() => {
    if (activeView === 'routes') {
        handleFetchRoutes();
    }
}, [activeView]);

const handleExtractText = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
        const response = await fetch('http://api.andrabima.my.id/api/v1/consolidate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ raw_text: smartText })
        });
        
        if (response.ok) {
            const data = await response.json();
            setFormData(data.extracted_data);
        } else {
            throw new Error('API Extractor Not Ready ⚠');
        }
    } 

    // Tester
    catch (err) {
        console.log("Menggunakan fallback extraksi lokal untuk demo...")

        setFormData({
            origin: 'Jakarta',
            destination: 'Surabaya',
            date: '2026-07-20',
            item_name: 'Sagu',
            volume_m3: '8',
            weight_tons: '5'
        });
    } 
   
    finally {
        setLoading(false);
        setActiveView('preview');
    }
};

// Fungsi Match
const handleFindMatch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
        const response = await fetch('http://api.andrabima.my.id/api/v1/consolidate-confirmed', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (response.status === 400 || response.status === 422) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Validasi gagal atau barang berbahaya.');
        } else if (response.status == 502) {
            throw new Error('Terjadi kesalahan server, silahkan coba lagi.');
        } else if (!response.ok) {
            throw new Error('Gagal menghubungi server.');
        }

        const data = await response.json();
        setMatchData(data);
    } 
    
    catch (err) {
        // Mock data jika server mati (DEMO UI)
        if (err.message.includes('Failed to fetch') || err.message.includes('API')) {
            setMatchData({
                status: 'SUCCESS', // atau ganti ke 'NO_MATCH_DEDICATED_CONTAINER'
                match: { id: 'M-1', sisa_slot: '3 Ton', eta: '27 Juli 2026', harga: 'Rp. 2.500.00' },
                alternatives: [
                    { id: 'A-1', sisa_slot: '5 Ton', eta: '29 Juli 2026', harga: 'Rp. 2.100.00'}
                ],
                pricing: { dedicated_container_price_idr: 'Rp. 15.000.00' },
                recommended_split_price_idr: 'Rp. 2.500.000'
            });
        } else {
            setErrorMsg(err.message);
            setLoading(false);
            return;
        }
    }

    setLoading(false);
    setActiveView('match');
};

const handleBooking = (selectedSlot) => {
    const newOrder = {
        ...formData,
        ...selectedSlot,
        price: matchData.pricing.recommended_split_price_idr,
        status: 'Menunggu Pembayaran',
        resi: `INV-${Math.floor(Math.random() * 100000)}`
    };
    setOrders([...orders, newOrder]);
    alert('Berhasil booking slot!');
    setActiveView('orders');
    setShowAlternative(false);
};

const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
};

const addDaysToDate = (dateString, days) => {
    const date = new Date(dateString);  // ⬅️ buat objek Date BARU dari string
    date.setDate(date.getDate() + days); // ⬅️ ini cuma ubah objek BARU tadi
    return date.toLocaleDateString('id-ID', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
    });
};

const formatRupiah = (num) => {
    if (num === undefined || num === null) return 'Hubungi CS';
    return `Rp ${num.toLocaleString('id-ID')}`;
};

return (
        <div className="app-layout">
            
        <header className="top-navbar">
            <div className="nav-container">
                <div className='nav-brand'><h2>Nusantara Match</h2></div>
                <nav className='nav-links'>
                    <button onClick={() => setActiveView('input')} className={activeView === 'input' ? 'active' : ''}>Cari Kapal</button>
                    <button onClick={() => setActiveView('routes')} className={activeView === 'routes' ? 'active' : ''}>List Rute</button>
                    <button onClick={() => setActiveView('orders')} className={activeView === 'orders' ? 'active' : ''}>Pesanan ({orders.length})</button>
                </nav>
            </div>
        </header>

        <main className='main-content'>
            <div className='content-card'>

                {/* Tampilan Error */}
                {errorMsg && <div className='error-alert'>⚠ {errorMsg}</div>}

                {/* LANGKAH 1: FORMULIR */}
                {activeView === 'input' && (
                    <div className='form-section'>
                        <h3 className='section-title'>Pencarian AI</h3>
                        <p className='helper-text'>Ketik kebutuhan logistik anda, AI kami akan memproseskannya untuk anda</p>

                        <form onSubmit={handleExtractText}>
                            <textarea
                                className='smart-textarea'
                                rows="4"
                                placeholder='Contoh: "Halo, saya mau kirim tekstil 8 m3 berat 5 ton dari Jakarta ke Surabaya tanggal 20 Juli 2026."'
                                value={smartText}
                                onChange={(e) => setSmartText(e.target.value)}
                                required
                            />
                            <button type='submit' className='btn-primary' disabled={loading}>
                                {loading ? 'Menganalisis Teks...' : 'Ekstrak dengan AI...'}
                            </button>
                        </form>
                    </div>
                )}

                {/* LANGKAH 2: MATCHING CARD*/}
                {activeView === 'preview' && (
                    <div className='form-section'>
                        <h3 className='section-title'>Cek & Koreksi Data</h3>
                        <p className='helper-text'>Berikut adalah data yang terbaca. Silahkan koreksi jika ada yang kurang tepat.</p>

                        <form onSubmit={handleFindMatch}>
                            <div className='input-group'>
                                <label>Pelabuhan Asal</label>
                                <input name='origin' value={formData.origin} onChange={handleInputChange} required />
                            </div>
                            <div className='input-group'>
                                <label>Pelabuhan tujuan</label>
                                <input name='destination' value={formData.destination} onChange={handleInputChange} required />
                            </div>
                            <div className='input-group'>
                                <label>Tanggal Pengiriman</label>
                                <input type='date' name='date' value={formData.date} onChange={handleInputChange} required placeholder='Cth: 25 Juli 2026' />
                            </div>
                            <div className='input-group'>
                                <label>Nama Barang</label>
                                {formData.item_name === 'Barang tidak teridentifikasi' && <span className='text-warning'>⚠ Gagal diekstrak</span>}
                                <input name='item_name' value={formData.item_name} onChange={handleInputChange} required />
                            </div>
                            <div className='input-group'>
                                <label>Volume M3</label>
                                <input name='volume_m3' value={formData.volume_m3} onChange={handleInputChange} required placeholder='Cth: 2 m3' />
                            </div>
                            <div className='input-group'>
                                <label>Berat (Tons)</label>
                                <input name='weight_tons' value={formData.weight_tons} onChange={handleInputChange} required placeholder='Cth: 500 KG' />
                            </div>

                            <div className='action-row'>
                                <button type='button' onClick={() => setActiveView('input')} className='btn-secondary'>Kembali</button>
                                <button type='submit' className='btn-primary' disabled={loading}>
                                    {loading ? 'Memeriksa Keamanan...' : 'Cari Slot Match...'}
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                {/* LANGKAH 3: HASIL MATCH & ALTERNATIF */}
                {activeView === 'match' && matchData && (
                    <div className='match-session'>
                        <h3 className='section-title'>Hasil Pencocokan AI</h3>

                        {/* KONDISI 1: TIDAK ADA SLOT LCL / DEDICATED ONLY */}
                        {matchData.status === 'NO_MATCH_DEDICATED_CONTAINER' || !matchData.match ? (
                            <div className='dedicated-warning'>
                                <h4>⚠ Tidak ada slot gabungan (LCL)</h4>
                                <p>Tidak ada kontainer dengan rute dan jadwal yang sesuai untuk digabungkan dengan barang Anda.</p>
                                <div className='dedicated-price'>
                                    <span>Saran: Sewa Kontainer Penuh (FCL)</span>
                                    <strong>{formatRupiah(matchData.pricing?.dedicated_container_price_idr) || 'Hubungi CS'}</strong>
                                </div>
                                <button onClick={() => setActiveView('input')} className='btn-primary' style={{marginTop: '15px'}}>Cari Ulang</button>
                            </div>
                        ) : (
                            /* KONDISI 2: MATCH DITEMUKAN */
                            <>
                            <div className='best-match-card'>
                                <div className='match-badge'>Saran Terbaik (Anonim)</div>
                                <div className='card-body'>
                                    <h4>Slot Kapal Tersedia</h4>
                                    <div className='route'><span>{formData.origin}</span> ➜ <span>{formData.destination}</span></div>
                                    <div className='details'>
                                        <p><strong>Sisa Volume:</strong> {matchData.match.remaining_volume_m3} m³</p>
                                        <p><strong>Sisa Berat:</strong> {matchData.match.remaining_weight_tons} Tons</p>
                                        <p><strong>Estimasi Tiba:</strong> {addDaysToDate(matchData.match.consolidation_date, matchData.match.eta_min_days)} - {addDaysToDate(matchData.match.consolidation_date, matchData.match.eta_max_days)} </p>
                                    </div>
                                    <div className='price-tag'>{formatRupiah(matchData.pricing?.recommended_split_price_idr)}</div>
                                    <button onClick={() => handleBooking(matchData.match)} className='btn-book-match'>Pesan Slot Ini</button>
                                </div>
                            </div>

                            {/* KONDISI ALTERNATIF */}
                            {matchData.alternatives && matchData.alternatives.length > 0 && (
                                <div className='alternative-section'>
                                    {matchData.alternatives.map((alt) => (
                                        <div key={alt.anonymous_slot_reference} className='alt-card'>
                                            <div>
                                                <p><strong>ETA:</strong> {addDaysToDate(alt.consolidation_date, alt.eta_min_days)} - {addDaysToDate(alt.consolidation_date, alt.eta_max_days)}</p>
                                                <p className='alt-price'>{alt.harga}</p>
                                            </div>
                                            <button onClick={() => handleBooking(alt)} className='btn-book-alt'>Pilih</button>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}
                </div>
            )}
                    
                    {/* LANGKAH 4: HALAMAN PESANAN & TRACKING*/}
                    {activeView === 'orders' && (
                        <div className='orders-section'>
                            <h3 className='section-title'>Daftar Pesanan</h3>
                            {orders.length === 0 ? (
                                <p className='empty-state'>Belum ada pesanan aktif.</p>
                            ) : (
                                orders.map((order, index) => (
                                    <div key={index} className='order-card'>
                                        <div className='order-header'>
                                            <strong>{order.resi}</strong>
                                            <span className='badge'>{order.status}</span>
                                        </div>
                                        <div className='order-details'>
                                            <p><strong>Rute:</strong> {order.origin} - {order.destination}</p>
                                            <p><strong>Barang:</strong> {order.item_name}, ({order.weight_tons} Tons)</p>
                                            <p><strong>Biaya:</strong> <span style={{color: '#2e7d32', fontWeight:'bold'}}>{formatRupiah(order.price)}</span></p>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    )}

                    {/* Route List */}
                    {activeView === 'routes' && (
                        <div className='route-section'>
                            <h3 className='section-title'>Daftar Kapal Tersedia</h3>
                            <p className='helper-text'> Berikut rute dan kapasitas kapal yang tersedia saat ini</p>

                            {loadingRoutes ? (
                                <p className='empty-state'>Memuat data...</p>
                            ) : routes.length === 0 ? (
                                <p className='empty-state'>Belum ada rute tersedia.</p>
                            ) : (
                                routes.map((route, index) => (
                                    <div key={index} className='route-card'>
                                        <div className='route'>
                                            <span>{route.origin}</span>
                                            <span>~~~~~~~⏅</span>
                                            <span>{route.destination}</span>
                                        </div>
                                        <div className='route-details'>
                                            <p><strong>Tanggal:</strong> {route.date}</p>
                                            <p><strong>Sisa Volume:</strong> {route.available_volume_m3}</p>
                                            <p><strong>Sisa Berat:</strong> {route.available_weight_tons}</p>
                                            <p><strong>Utilisasi Ruang:</strong> {route.space_utilization_percent}</p>
                                            <p><strong>ETA:</strong> {addDaysToDate(route.date, route.eta_min_days)} - {addDaysToDate(route.date, route.eta_max_days)}</p>
                                        </div>
                                    </div>
                                ))
                            )
                        }
                        </div>
                    )}

            </div>
        </main>

            <footer className='bottom-footer'>
                <div className='footer-content'>
                    <p>&copy; 2026 Nusantara Match - Solusi Logistik Maritim Indonesia.</p>
                    <div className='footer-links'>
                        <a href='#bantuan'>Pusat Bantuan</a>
                        <a href='#syarat'>Syarat & Ketentuan</a>
                        <a href='#privasi'>Kebijakan Privasi</a>
                    </div>
                </div>
            </footer>
    </div>
)
};

export default LogiMatch;