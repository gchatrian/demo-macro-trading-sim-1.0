#!/usr/bin/env python3
"""
Test Terminal Output Manager
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from controller.terminal_output_manager import TerminalOutputManager


def test_terminal_output_manager():
    """Test terminal output manager functionality"""
    print("=" * 60)
    print("Terminal Output Manager Test")
    print("=" * 60)
    
    # Initialize manager
    print("\n1. Initializing Terminal Output Manager...")
    output = TerminalOutputManager(use_colors=True)
    print("   ✓ Manager initialized")
    
    # Test 2: Welcome banner
    print("\n2. Testing welcome banner...")
    output.print_welcome()
    print("   ✓ Welcome banner displayed")
    
    # Test 3: Headers
    print("\n3. Testing headers...")
    sim_time = datetime(2025, 1, 15, 14, 30, 0)
    output.print_header("Test Header", sim_time)
    print("   ✓ Header displayed")
    
    # Test 4: System logs
    print("\n4. Testing system logs...")
    output.print_system_log("Initialization complete", "SUCCESS", sim_time)
    output.print_system_log("Processing data...", "INFO", sim_time)
    output.print_system_log("High volatility detected", "WARNING", sim_time)
    output.print_system_log("Connection failed", "ERROR", sim_time)
    print("   ✓ System logs displayed")
    
    # Test 5: Macro state
    print("\n5. Testing macro state display...")
    output.print_macro_state(
        growth=2.8,
        inflation=2.5,
        volatility=15.3,
        regime="Goldilocks: Strong growth with moderate inflation",
        sim_datetime=sim_time
    )
    print("   ✓ Macro state displayed")
    
    # Test 6: Pre-release narrative
    print("\n6. Testing pre-release narrative...")
    pre_release_content = """
Markets are bracing for tomorrow's Non-Farm Payrolls release, with consensus 
estimates pointing to 180,000 new jobs. Analysts are divided on whether the 
labor market's resilience will continue or show signs of cooling.

The Federal Reserve has indicated that employment data will be crucial in 
determining their next policy move. A strong beat could reignite inflation 
concerns, while a miss might signal economic softening.
"""
    
    event_info = {
        'name': 'Non-Farm Payrolls January',
        'consensus': 180.0
    }
    
    output.print_narrative(
        narrative_type='pre_release',
        content=pre_release_content.strip(),
        event_info=event_info,
        sim_datetime=sim_time
    )
    print("   ✓ Pre-release narrative displayed")
    
    # Test 7: Post-release narrative
    print("\n7. Testing post-release narrative...")
    post_release_content = """
The labor market just delivered a significant upside surprise, with 215,000 
jobs added in January, well above the 180,000 consensus. This robust print 
suggests the economy retains considerable momentum despite elevated interest 
rates.

Market reaction was swift: yields jumped 10 basis points as traders repriced 
Fed expectations, while equities initially dipped on renewed tightening fears 
before recovering on growth optimism. The dollar strengthened across the board.
"""
    
    event_info_post = {
        'name': 'Non-Farm Payrolls January',
        'consensus': 180.0,
        'actual': 215.0
    }
    
    output.print_narrative(
        narrative_type='post_release',
        content=post_release_content.strip(),
        event_info=event_info_post,
        sim_datetime=sim_time
    )
    print("   ✓ Post-release narrative displayed")
    
    # Test 8: Event narrative
    print("\n8. Testing event narrative...")
    event_content = """
In a surprise announcement today, major tech companies unveiled a breakthrough 
in artificial intelligence that promises to dramatically boost productivity 
across sectors. The new technology could reshape economic dynamics over the 
coming quarters.

Initial market reaction has been euphoric, with tech stocks surging on the 
news. However, economists caution that the full implications for growth and 
inflation will take time to materialize. The Fed will likely monitor 
developments closely.
"""
    
    event_info_macro = {
        'headline': 'Major Tech Companies Announce Revolutionary AI Breakthrough'
    }
    
    output.print_narrative(
        narrative_type='event',
        content=event_content.strip(),
        event_info=event_info_macro,
        sim_datetime=sim_time
    )
    print("   ✓ Event narrative displayed")
    
    # Test 9: Progress bar
    print("\n9. Testing progress indicator...")
    output.print_progress(25, 100, "Processing events")
    output.print_progress(50, 100, "Halfway through")
    output.print_progress(75, 100, "Almost done")
    output.print_progress(100, 100, "Complete")
    print("   ✓ Progress indicators displayed")
    
    # Test 10: Goodbye
    print("\n10. Testing goodbye message...")
    output.print_goodbye()
    print("   ✓ Goodbye message displayed")
    
    print("\n" + "=" * 60)
    print("✓ All Terminal Output Manager tests passed!")
    print("=" * 60)
    print("\nNote: Check that colors and formatting look good in your terminal.")
    
    return True


if __name__ == "__main__":
    success = test_terminal_output_manager()
    exit(0 if success else 1)
