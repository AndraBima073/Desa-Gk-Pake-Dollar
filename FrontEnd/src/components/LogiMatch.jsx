import React, { use, useState } from 'react';
import '../styles/LogiMatch.css';

const LogiMatch = () => {
    const [activeView, setActiveView] = useState('input');
    const [shippingMode, setShippingMode] = useState('FCL');
    const [formData, setFormData] = useState({ asal: '', tujuan: '', tanggal: '', barang: ''});
    const [orders, setOrders] = useState([]);


const ships = [
    { id: 1, p: 'PT Pelni', k: 'KM Kelud', sisa: 2, harga: 'Rp 15.000.000', eta: '22 Juli 2026' },
    { id: 2, p: 'PT Samudera Indonesia', k: 'Sinar Sumba', sisa: 5, harga: '14.500.000', eta: '23 Juli 2026' },
    { id: 3, p: 'Meratus', k: 'Meratus Jimbaran', sisa: 1, harga: 'Rp 13.800.000', eta: '24 Jul 2026' },
    { id: 4, p: 'Temas Line', k: 'Temas Jakarta', sisa: 10, harga: 'Rp 12.500.000', eta: '25 Jul 2026' },
    { id: 5, p: 'Pertamina PIS', k: 'MT Gamsunoro', sisa: 3, harga: 'Rp 18.000.000', eta: '26 Jul 2026' },
    { id: 6, p: 'SPIL', k: 'Spil Ningsih', sisa: 8, harga: 'Rp 14.000.000', eta: '27 Jul 2026' },
    { id: 7, p: 'Tanto Intim Line', k: 'Tanto Bersatu', sisa: 4, harga: 'Rp 13.500.000', eta: '28 Jul 2026' },
    { id: 8, p: 'Bahana Line', k: 'Bahana 1', sisa: 6, harga: 'Rp 11.000.000', eta: '29 Jul 2026' },
    { id: 9, p: 'Waruna Nusa Sentana', k: 'Waruna 3', sisa: 2, harga: 'Rp 16.000.000', eta: '30 Jul 2026' },
    { id: 10, p: 'Logindo Samudramakmur', k: 'Logindo 5', sisa: 7, harga: 'Rp 12.000.000', eta: '31 Jul 2026' },
    { id: 11, p: 'PPNP', k: 'PPNP Express', sisa: 12, harga: 'Rp 10.500.000', eta: '01 Agt 2026' }
];

const [currentShipIndex, setCurrentShipIndex] = useState(0);

const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
};

const handleSearch = (e) => {
    e.preventDefault();
    setActiveView('match');
};

const handleSwipe = (action) => {
    if (action === 'match') {
        const newOrder = {
            ...ships[currentShipIndex],
            ...formData,
            mode: shippingMode,
            status: 'Sedang Berlayar',
            resi: `INV-${Math.floor(Math.random() * 100000)}`
        };
        setOrders([...orders, newOrder]);
        alert(`Berhasil booking di ${ships[currentShipIndex].p}! Membuka halaman pesanan...`);
        setActiveView('orders');
    }else{
        if (currentShipIndex < ships.length - 1){
            setCurrentShipIndex(currentShipIndex + 1);
        } else {
            alert('Tidak ada jawal kapal lain saat ini. Silahkan ubah kriteria pencarian');
            setActiveView('input');
            setCurrentShipIndex(0);
        }
    }
};

return (
    <div className="logimatch-wrapper">
        <div className="">
            
            <header className="header">
                <h2>Nusantara Match</h2>
                <nav>
                    <button onClick={() => setActiveView('input')} className={activeView === 'input' ? 'active' : ''}>Cari</button>
                    <button onClick={() => setActiveView('orders')} className={activeView === 'orders' ? 'active' : ''}>Pesanan ({orders.length})</button>
                </nav>
            </header>

            <div className='content'>

                {/* LANGKAH 1: FORMULIR */}
                {activeView === 'input' && (
                    <div className='form-section'>
                        <div className='tabs'>
                            <button className={shippingMode === 'FCL' ? 'tab active' : 'tab'} onClick={() => setShippingMode('FCL')}>Sewa Full (FCL)</button>
                            <button className={shippingMode === 'LCL' ? 'tab active' : 'tab'} onClick={() => setShippingMode('LCL')}>Split Container (LCL)</button>
                        </div>

                        <form onSubmit={handleSearch}>
                            {shippingMode === 'LCL' && (
                                <div className='info-box'>
                                    Barang Anda akan digabungkan secara anonim dengan pengirim lain dalam satu kontainer untuk menghemat biaya.
                                </div>
                            )}

                            <div className='input-group'>
                                <label>Pelabuhan Asal</label>
                                <input name='asal' required placeholder='Cth: Tanjung Priok' onChange={handleInputChange} />
                            </div>

                            <div className='input-group'>
                                <label>Pelabuhan Tujuan</label>
                                <input name='tujuan' required placeholder='Cth: Tanjung Perak' onChange={handleInputChange} />
                            </div>

                            <div className='input-group'>
                                <label>Waktu Pengiriman</label>
                                <input type='date' name='tanggal' required onChange={handleInputChange}/>
                            </div>

                            <div className='input-group'>
                                <label>{shippingMode === 'FCL' ? 'Isi Kontainer' : 'Deskripsi & Volume Barang (CBM)'}</label>
                                <input name='barang' required placeholder={shippingMode === 'FCL' ? 'Cth: Elektronik 20ft' : 'Cth: 5 CBM Sparepart Motor'} onChange={handleInputChange}/>
                            </div>

                            <button type='submit' className='btn-primary'>Cari Kapal</button>
                        </form>
                    </div>
                )}

                {/* LANGKAH 2: MATCHING CARD*/}
                {activeView === 'match' && (
                    <div className='match-section'>
                        <div className='swipe-card'>
                            <div className='card-header'>
                                <h3>{ships[currentShipIndex].p}</h3>
                                <p>{ships[currentShipIndex].k}</p>
                            </div>
                            
                            <div className='card-body'>
                                <div className='route'>
                                    <span>{formData.asal}</span> <span>{formData.tujuan}</span>
                                </div>
                                <div className='details'>
                                    <p><strong>Mode:</strong> {shippingMode}</p>
                                    <p><strong>Sisa Slot:</strong> {ships[currentShipIndex].sisa} {shippingMode === 'FCL' ? 'TEU' : 'CBM Space'}</p>
                                    <p><strong>ETA:</strong>{ships[currentShipIndex].eta}</p>
                                </div>
                                <div className='price'>{ships[currentShipIndex].harga}</div>
                            </div>
                        </div>

                        <div className='action-row'>
                            <button onClick={() => handleSwipe('skip')} className='btn-skip'>X Skip</button>
                            <button onClick={() => handleSwipe('match')} className='btn-match'>V Match</button>
                        </div>
                    </div>
                )}
                    
                    {/* LANGKAH 3: HALAMAN PESANAN & TRACKING*/}
                    {activeView === 'orders' && (
                        <div className='orders-section'>
                            <h3>Daftar Pesanan</h3>
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
                                            <p><strong>Kapal:</strong> {order.k} ({order.p})</p>
                                            <p><strong>Rute:</strong> {order.asal} - {order.tujuan}</p>
                                            <p><strong>ETA:</strong> {order.eta}</p>
                                        </div>
                                        <div className='order-selection'>
                                            <button onClick={() => alert('Membuka Peta Pelacakan GPS...')} className='btn-track'>Lacak Posisi</button>
                                            <button onClick={() => alert(`Mengunduh Invoice untuk ${order.resi}...`)} className='btn-invoice'>Unduh Invoice</button>
                                        </div>
                                    </div>
                                ))
                            )
                        }
                        </div>
                    )}
                </div>
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
    </div>
)
}
export default LogiMatch;