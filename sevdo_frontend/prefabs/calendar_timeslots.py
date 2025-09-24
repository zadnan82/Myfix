# sevdo_frontend/prefabs/calendar_timeslots.py
def render_prefab(args, props):
    title = props.get("title", "Book a Timeslot")
    slot_minutes = int(str(props.get("slotMinutes", "30")) or "30")
    open_time = props.get("open", "09:00")
    close_time = props.get("close", "17:00")
    start_date = props.get("start")
    storage_key = props.get("storageKey", "sevdoTimeslots")

    # Accept inline args like: cal(open=08:00, close=18:00, slotMinutes=30)
    if args and "=" in args:
        parts = [p.strip() for p in args.split(",") if p.strip()]
        inline = {}
        for p in parts:
            if "=" in p:
                k, v = p.split("=", 1)
                inline[k.strip()] = v.strip()
        if "slotMinutes" in inline:
            try:
                slot_minutes = int(str(inline["slotMinutes"]).strip() or "30")
            except Exception:
                slot_minutes = 30
        if "open" in inline:
            open_time = inline["open"]
        if "close" in inline:
            close_time = inline["close"]
        if "start" in inline:
            start_date = inline["start"]

    # Optional backend echo props (for future)
    book_path = props.get("bookPath") or "/api/echo"
    book_method = (props.get("bookMethod") or "POST").upper()
    unbook_path = props.get("unbookPath") or "/api/echo"
    unbook_method = (props.get("unbookMethod") or "POST").upper()
    book_action = props.get("bookAction") or ""
    unbook_action = props.get("unbookAction") or ""

    # Generate React component with proper hooks instead of DOM manipulation
    # Use safe string formatting to avoid f-string conflicts

    # Create the JavaScript template using string concatenation
    js_template = '''
import { useState, useEffect } from 'react';

function CalendarContent() {
    const [weekOffset, setWeekOffset] = useState(0);
    const [bookings, setBookings] = useState({});
    const [currentWeekLabel, setCurrentWeekLabel] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Utility functions
    const parseHM = (s) => {
        const parts = String(s).split(':');
        const hh = parseInt(parts[0] || '0', 10);
        const mm = parseInt(parts[1] || '0', 10);
        return hh * 60 + mm;
    };

    const fmtHM = (m) => {
        const h = Math.floor(m / 60);
        const mm = String(m % 60).padStart(2, '0');
        return String(h).padStart(2, '0') + ':' + mm;
    };

    const startOfWeek = (d) => {
        const dt = new Date(d.getFullYear(), d.getMonth(), d.getDate());
        const wd = (dt.getDay() + 6) % 7;
        dt.setDate(dt.getDate() - wd);
        dt.setHours(0, 0, 0, 0);
        return dt;
    };

    const weekKey = (dt) => {
        const y = dt.getFullYear();
        const m = String(dt.getMonth() + 1).padStart(2, '0');
        const dd = String(dt.getDate()).padStart(2, '0');
        return y + '-' + m + '-' + dd;
    };

    // Load bookings from localStorage
    useEffect(() => {
        load();
    }, []);

    const load = () => {
        try {
            const raw = localStorage.getItem('''' + storage_key + '''');
            if (raw) {
                setBookings(JSON.parse(raw));
            }
        } catch (e) {
            console.error('Error loading bookings:', e);
        } finally {
            setLoading(false);
        }
    };

    const save = (data) => {
        try {
            localStorage.setItem('''' + storage_key + '''', JSON.stringify(data));
            setBookings(data);
        } catch (e) {
            console.error('Error saving bookings:', e);
        }
    };

    const echo = (msg) => {
        if (window.sevdoAct) {
            window.sevdoAct('echo|' + JSON.stringify({ msg: msg, ts: Date.now() }));
        }
    };

    const render = () => {
        const base = ''' + (repr(start_date) if start_date else 'null') + ''' ? new Date(''' + (repr(start_date) if start_date else 'null') + ''' + 'T00:00:00') : new Date();
        const sow = startOfWeek(base);
        sow.setDate(sow.getDate() + 7 * weekOffset);

        const week = [];
        for (let i = 0; i < 7; i++) {
            const date = new Date(sow);
            date.setDate(sow.getDate() + i);
            week.push(date);
        }

        const weekStart = week[0];
        const weekEnd = week[6];
        const wkey = weekKey(weekStart);
        const weekData = bookings[wkey] || {};

        setCurrentWeekLabel(weekStart.toISOString().slice(0, 10) + ' - ' + weekEnd.toISOString().slice(0, 10));

        const openM = parseHM(''' + repr(open_time) + ''');
        const closeM = parseHM(''' + repr(close_time) + ''');
        const rows = Math.max(0, Math.floor((closeM - openM) / ''' + str(slot_minutes) + '''));

        const gridRows = [];
        for (let r = 0; r < rows; r++) {
            const row = [];

            // Time column
            row.push(
                <div key={'time-' + r} className="bg-white p-2 text-xs text-gray-500 border-r border-gray-200">
                    {fmtHM(openM + r * ''' + str(slot_minutes) + ''')}
                </div>
            );

            // Day columns
            for (let d = 0; d < 7; d++) {
                const daySlots = weekData['d' + d] || [];
                const isBooked = daySlots.includes(r);

                const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                const dayName = dayNames[d];
                const dateStr = week[d].toISOString().slice(0, 10);

                row.push(
                    <button
                        key={'slot-' + d + '-' + r}
                        className={'p-2 text-xs text-center border-r border-gray-200 ' + (isBooked
                                ? 'bg-green-600 text-white hover:bg-green-700'
                                : 'bg-white text-gray-700 hover:bg-gray-50'
                        )}
                        onClick={() => handleSlotClick(d, r, wkey, weekData)}
                        title={dayName + ' ' + dateStr + ' at ' + fmtHM(openM + r * ''' + str(slot_minutes) + ''')}
                    >
                        {isBooked ? '✓' : ''}
                    </button>
                );
            }

            gridRows.push(
                <div key={r} className="grid grid-cols-8 bg-gray-100">
                    {row}
                </div>
            );
        }

        return gridRows;
    };

    const handleSlotClick = (dayIndex, slotIndex, wkey, weekData) => {
        const daySlots = weekData['d' + dayIndex] || [];
        const slotIndexInArray = daySlots.indexOf(slotIndex);
        let newBookings = {...bookings};

        if (slotIndexInArray >= 0) {
            // Unbook slot
            weekData['d' + dayIndex] = daySlots.filter(idx => idx !== slotIndex);
            newBookings[wkey] = weekData;

            const slotTime = fmtHM(parseHM(''' + repr(open_time) + ''') + slotIndex * ''' + str(slot_minutes) + ''');
            const payload = {
                event: 'unbook',
                week: wkey,
                day: dayIndex,
                time: slotTime,
                ts: Date.now()
            };
            handleBookingAction('unbook', payload);
        } else {
            // Book slot
            weekData['d' + dayIndex] = [...daySlots, slotIndex];
            newBookings[wkey] = weekData;

            const slotTime = fmtHM(parseHM(''' + repr(open_time) + ''') + slotIndex * ''' + str(slot_minutes) + ''');
            const payload = {
                event: 'book',
                week: wkey,
                day: dayIndex,
                time: slotTime,
                ts: Date.now()
            };
            handleBookingAction('book', payload);
        }

        save(newBookings);
    };

    const handleBookingAction = (kind, payload) => {
        if (kind === 'book' && ''' + repr(book_action) + ''') {
            if (window.sevdoAct) {
                window.sevdoAct(''' + repr(book_action) + ''');
            }
            return;
        }
        if (kind === 'unbook' && ''' + repr(unbook_action) + ''') {
            if (window.sevdoAct) {
                window.sevdoAct(''' + repr(unbook_action) + ''');
            }
            return;
        }

        // API call
        const path = kind === 'book' ? ''' + repr(book_path) + ''' : ''' + repr(unbook_path) + ''';
        const method = kind === 'book' ? ''' + repr(book_method) + ''' : ''' + repr(unbook_method) + ''';
        if (window.sevdoAct) {
            window.sevdoAct('api:' + method + ' ' + path + '|' + JSON.stringify(payload));
        }
    };

    const navigateWeek = (delta) => {
        setWeekOffset(prev => prev + delta);
    };

    if (loading) {
        return (
            <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Loading calendar...</p>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto px-4">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900">''' + repr(title) + '''</h2>
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => navigateWeek(-1)}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1.5 rounded text-sm transition-colors"
                    >
                        ← Prev
                    </button>
                    <div className="text-sm text-gray-600 min-w-[220px] text-center font-medium">
                        {currentWeekLabel}
                    </div>
                    <button
                        onClick={() => navigateWeek(1)}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1.5 rounded text-sm transition-colors"
                    >
                        Next →
                    </button>
                </div>
            </div>

            <div className="rounded-md overflow-hidden border border-gray-200">
                <div className="grid grid-cols-8 bg-gray-50 border-b border-gray-200">
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200">Time</div>
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200 text-center">Sun</div>
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200 text-center">Mon</div>
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200 text-center">Tue</div>
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200 text-center">Wed</div>
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200 text-center">Thu</div>
                    <div className="p-2 text-sm font-medium text-gray-700 border-r border-gray-200 text-center">Fri</div>
                    <div className="p-2 text-sm font-medium text-gray-700 text-center">Sat</div>
                </div>
                {render()}
            </div>

            <div className="mt-3 text-xs text-gray-500">
                Slot: ''' + str(slot_minutes) + ''' min • Open: ''' + repr(open_time) + ''' • Close: ''' + repr(close_time) + '''
            </div>
        </div>
    );
}

export default function CalendarTimeslots() {
    return (
        <section className="py-6 bg-white rounded-lg border">
            <CalendarContent />
        </section>
    );
}'''

    return js_template


# Register with token "ct"
COMPONENT_TOKEN = "ct"